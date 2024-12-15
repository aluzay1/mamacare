const patientPIN = "1234";
const medicalRecordsSection = document.getElementById("medicalRecords");
const pinError = document.getElementById("pinError");

document.getElementById("pinForm").addEventListener("submit", (e) => {
    e.preventDefault();
    const enteredPIN = document.getElementById("patientPin").value;

    if (enteredPIN === patientPIN) {
        medicalRecordsSection.style.display = "block";
        document.querySelector(".auth-section").style.display = "none";
    } else {
        pinError.style.display = "block";
    }
});

const records = [
    { date: "2024-12-01", diagnosis: "Fever", treatment: "Rest", medication: "Paracetamol", doctor: "Dr. Smith", hospital: "City General" },
];

function renderRecords() {
    const tableBody = document.getElementById("recordsTableBody");
    tableBody.innerHTML = "";
    records.forEach((record, index) => {
        const row = `
            <tr>
                <td>${record.date}</td>
                <td>${record.diagnosis}</td>
                <td>${record.treatment}</td>
                <td>${record.medication}</td>
                <td>${record.doctor}</td>
                <td>${record.hospital}</td>
                <td><button onclick="deleteRecord(${index})">Delete</button></td>
            </tr>
        `;
        tableBody.innerHTML += row;
    });
}

document.getElementById("addRecordForm").addEventListener("submit", (e) => {
    e.preventDefault();
    const record = {
        date: document.getElementById("date").value,
        diagnosis: document.getElementById("diagnosis").value,
        treatment: document.getElementById("treatment").value,
        medication: document.getElementById("medication").value,
        doctor: document.getElementById("doctor").value,
        hospital: document.getElementById("hospital").value,
    };
    records.push(record);
    renderRecords();
    e.target.reset();
});

function deleteRecord(index) {
    records.splice(index, 1);
    renderRecords();
}

document.addEventListener("DOMContentLoaded", renderRecords);

function navigateToAddPatient() {
    window.location.href = "add_patient.html";
}