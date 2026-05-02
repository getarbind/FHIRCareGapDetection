import streamlit as st
import requests
from datetime import date, datetime
from typing import Any, Dict, List, Optional

st.title("Fetch Patient from FHIR Server")
st.write("Search and import patient data from a FHIR server.")

if "imported_patients" not in st.session_state:
    st.session_state["imported_patients"] = {}

if "patient_search_results" not in st.session_state:
    st.session_state["patient_search_results"] = []


def find_resource(data: Dict[str, Any], resource_type: str) -> Optional[Dict[str, Any]]:
    if data.get("resourceType") == resource_type:
        return data
    if data.get("resourceType") == "Bundle":
        for entry in data.get("entry", []):
            resource = entry.get("resource")
            if resource and resource.get("resourceType") == resource_type:
                return resource
    return None


def format_name(name: Dict[str, Any]) -> str:
    parts = []
    parts.extend(name.get("prefix", []))
    parts.extend(name.get("given", []))
    if name.get("family"):
        parts.append(name["family"])
    return " ".join(parts).strip()


def format_address(address: Dict[str, Any]) -> str:
    lines = []
    lines.extend(address.get("line", []))
    if address.get("city"):
        lines.append(address["city"])
    if address.get("state"):
        lines.append(address["state"])
    if address.get("postalCode"):
        lines.append(address["postalCode"])
    if address.get("country"):
        lines.append(address["country"])
    return ", ".join(lines)


def format_coding(coding_list: List[Dict[str, Any]]) -> str:
    display_values = [coding.get("display") or coding.get("code") for coding in coding_list]
    return ", ".join([v for v in display_values if v])


def parse_extensions(extensions: List[Dict[str, Any]]) -> Dict[str, Any]:
    parsed = {}
    for ext in extensions:
        url = ext.get("url", "")
        if url.endswith("us-core-race") or url.endswith("us-core-ethnicity"):
            nested = ext.get("extension", [])
            for item in nested:
                if item.get("url") == "text":
                    parsed[url] = item.get("valueString")
        elif url.endswith("patient-mothersMaidenName"):
            parsed["Mother's maiden name"] = ext.get("valueString")
        elif url.endswith("us-core-birthsex"):
            parsed["Birth sex"] = ext.get("valueCode")
        elif url.endswith("patient-birthPlace"):
            place = ext.get("valueAddress", {})
            parsed["Birth place"] = format_address(place)
        else:
            if "valueString" in ext:
                parsed[url] = ext.get("valueString")
            elif "valueCode" in ext:
                parsed[url] = ext.get("valueCode")
    return parsed


def format_identifiers(identifiers: List[Dict[str, Any]]) -> List[str]:
    formatted = []
    for identifier in identifiers:
        label = identifier.get("type", {}).get("text") or format_coding(
            identifier.get("type", {}).get("coding", [])
        )
        value = identifier.get("value")
        system = identifier.get("system")
        if label and value:
            formatted.append(f"{label}: {value}")
        elif value:
            formatted.append(value)
        elif system:
            formatted.append(system)
    return formatted


def calculate_age(birth_date: Optional[str]) -> Optional[int]:
    if not birth_date:
        return None
    try:
        parsed = datetime.fromisoformat(birth_date).date()
    except ValueError:
        try:
            parsed = datetime.strptime(birth_date, "%Y-%m-%d").date()
        except ValueError:
            return None
    today = date.today()
    return today.year - parsed.year - ((today.month, today.day) < (parsed.month, parsed.day))


def fetch_patient_by_id(base_url: str, patient_id: str) -> Dict[str, Any]:
    url = f"{base_url.rstrip('/')}/Patient/{patient_id}"
    response = requests.get(
        url,
        headers={"Accept": "application/fhir+json"},
        timeout=20
    )
    response.raise_for_status()
    return response.json()


def search_patients_by_name(base_url: str, family: str = "", given: str = "") -> Dict[str, Any]:
    url = f"{base_url.rstrip('/')}/Patient"
    params = {}
    if family:
        params["family"] = family
    if given:
        params["given"] = given

    response = requests.get(
        url,
        params=params,
        headers={"Accept": "application/fhir+json"},
        timeout=20
    )
    response.raise_for_status()
    return response.json()


def store_imported_patient(patient_key: str, data: Dict[str, Any]) -> None:
    existing = patient_key in st.session_state["imported_patients"]
    st.session_state["imported_patients"][patient_key] = data
    st.success(f"Patient data imported successfully! Stored as `{patient_key}`.")
    if existing:
        st.info("Existing import with the same key was overwritten.")


def render_imported_patients_list() -> None:
    st.subheader("Imported Patient Files")
    if not st.session_state["imported_patients"]:
        st.write("No imported patients yet.")
        return

    for key, data in st.session_state["imported_patients"].items():
        patient = find_resource(data, "Patient")
        if patient and patient.get("name"):
            label = format_name(patient["name"][0])
        else:
            label = key
        st.write(f"- {label} (key: {key})")


def render_patient_summary(data: Dict[str, Any]) -> None:
    patient = find_resource(data, "Patient")
    if not patient:
        st.warning("No Patient resource found in the imported data.")
        st.subheader("FHIR Data Preview")
        st.json(data)
        return

    st.subheader("Patient Summary")

    name = "N/A"
    if patient.get("name"):
        name = format_name(patient["name"][0])

    gender = patient.get("gender", "N/A").title()
    birth_date = patient.get("birthDate", "N/A")
    age = calculate_age(patient.get("birthDate"))
    marital_status = patient.get("maritalStatus", {}).get("text") or format_coding(
        patient.get("maritalStatus", {}).get("coding", [])
    )

    language = "N/A"
    if patient.get("communication"):
        language = patient["communication"][0].get("language", {}).get("text") or format_coding(
            patient["communication"][0].get("language", {}).get("coding", [])
        )

    extensions = parse_extensions(patient.get("extension", []))
    identifiers = format_identifiers(patient.get("identifier", []))
    telecom = [f"{item.get('system')}: {item.get('value')}" for item in patient.get("telecom", []) if
               item.get("value")]
    addresses = [format_address(address) for address in patient.get("address", []) if format_address(address)]

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Name:** {name}")
        st.markdown(f"**Gender:** {gender}")
        st.markdown(f"**Birth date:** {birth_date}")
        st.markdown(f"**Age:** {age if age is not None else 'N/A'}")
        st.markdown(f"**Language:** {language}")

    with col2:
        st.markdown(f"**Marital status:** {marital_status or 'N/A'}")
        st.markdown(f"**Primary phone:** {telecom[0] if telecom else 'N/A'}")
        st.markdown(f"**Address:** {addresses[0] if addresses else 'N/A'}")
        st.markdown(f"**Identifier count:** {len(identifiers)}")
        st.markdown(f"**Resource type:** {patient.get('resourceType')}")

    if identifiers:
        st.subheader("Identifiers")
        for identifier in identifiers:
            st.write(f"- {identifier}")

    if extensions:
        st.subheader("Demographic details")
        for label, value in extensions.items():
            st.write(f"- **{label.split('/')[-1].replace('-', ' ').title()}:** {value}")

    if len(addresses) > 1:
        st.subheader("Additional Addresses")
        for address in addresses[1:]:
            st.write(f"- {address}")

    if len(telecom) > 1:
        st.subheader("Additional Contact")
        for contact in telecom[1:]:
            st.write(f"- {contact}")

    if isinstance(data, dict) and data.get("resourceType") == "Bundle":
        st.subheader("Bundle Resources")
        counts = {}
        for entry in data.get("entry", []):
            resource_type = entry.get("resource", {}).get("resourceType")
            if resource_type:
                counts[resource_type] = counts.get(resource_type, 0) + 1
        for resource_type, count in counts.items():
            st.write(f"- {resource_type}: {count}")


# Main FHIR server section
base_url = st.text_input("FHIR Base URL", value="https://hapi.fhir.org/baseR4")
search_mode = st.radio("Search by", ["Patient ID", "Patient Name"])

if search_mode == "Patient ID":
    patient_id = st.text_input("Patient ID")

    if st.button("Fetch Patient by ID"):
        if not base_url.strip() or not patient_id.strip():
            st.warning("Please enter both FHIR Base URL and Patient ID.")
        else:
            try:
                data = fetch_patient_by_id(base_url, patient_id.strip())
                patient = find_resource(data, "Patient") or data
                patient_key = patient.get("id") or patient_id.strip()

                store_imported_patient(patient_key, data)
                render_patient_summary(data)

            except Exception as e:
                st.error(f"Error fetching patient: {e}")

elif search_mode == "Patient Name":
    family = st.text_input("Family name")
    given = st.text_input("Given name")

    if st.button("Search Patients"):
        if not base_url.strip():
            st.warning("Please enter the FHIR Base URL.")
        elif not family.strip() and not given.strip():
            st.warning("Please enter at least one of Family name or Given name.")
        else:
            try:
                result = search_patients_by_name(
                    base_url,
                    family=family.strip(),
                    given=given.strip()
                )

                entries = result.get("entry", [])
                st.session_state["patient_search_results"] = entries

                if not entries:
                    st.warning("No patients found.")
                else:
                    st.success(f"Found {len(entries)} patient(s).")

            except Exception as e:
                st.error(f"Error searching patients: {e}")

    entries = st.session_state.get("patient_search_results", [])
    if entries:
        options = {}
        for entry in entries:
            resource = entry.get("resource", {})
            patient_id = resource.get("id", "unknown")

            patient_name = "N/A"
            if resource.get("name"):
                patient_name = format_name(resource["name"][0])

            birth_date = resource.get("birthDate", "N/A")
            label = f"{patient_name} | ID: {patient_id} | DOB: {birth_date}"
            options[label] = resource

        selected_label = st.selectbox("Select a patient to import", list(options.keys()))

        if st.button("Import Selected Patient"):
            selected_patient = options[selected_label]
            patient_key = selected_patient.get("id", selected_label)

            store_imported_patient(patient_key, selected_patient)
            render_patient_summary(selected_patient)

st.markdown("---")
render_imported_patients_list()