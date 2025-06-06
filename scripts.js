const medicalRecordsSection = document.getElementById("medicalRecords");
const pinError = document.getElementById("pinError");

document.getElementById("pinForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const pin = document.getElementById("patientPin").value.trim();

    // Clear previous error
    pinError.style.display = "none";
    pinError.textContent = "";

    try {
        console.log('Attempting to access profile with PIN');
        
        // Now try to access the profile
        console.log('Sending profile request...');
        const requestData = { pin };
        console.log('Request data:', requestData);
        
        const response = await fetch('/api/patient/profile', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(requestData)
        });

        console.log('Response status:', response.status);
        const contentType = response.headers.get('content-type');
        console.log('Response content type:', contentType);
        console.log('Response headers:', Object.fromEntries(response.headers.entries()));

        // First get the raw response text
        const rawText = await response.text();
        console.log('Raw response:', rawText);

        // Check if the response is HTML
        if (rawText.trim().startsWith('<!DOCTYPE') || rawText.trim().startsWith('<html')) {
            console.error('Received HTML response instead of JSON');
            console.error('Response headers:', Object.fromEntries(response.headers.entries()));
            throw new Error('Server error: Received HTML response. Please try again later.');
        }

        // Try to parse as JSON
        let responseData;
        try {
            responseData = JSON.parse(rawText);
        } catch (e) {
            console.error('Error parsing response as JSON:', e);
            console.error('Raw response that failed to parse:', rawText);
            throw new Error('Invalid response from server. Please try again later.');
        }

        if (!response.ok) {
            throw new Error(responseData.error || 'Failed to access profile');
        }

        console.log('Received profile data:', responseData);
        
        // Store the user data
        localStorage.setItem('userData', JSON.stringify(responseData));
        
        // Show the medical records section
        medicalRecordsSection.style.display = "block";
        document.querySelector(".auth-section").style.display = "none";
        
        // Update the profile information
        updateProfileDisplay(responseData);
        
        // Update the medical records table
        updateMedicalRecordsTable(responseData.medical_records);
    } catch (error) {
        console.error('Profile access error:', error);
        pinError.textContent = `Error: ${error.message}. Please try again or contact support.`;
        pinError.style.display = "block";
    }
});

function updateProfileDisplay(userData) {
    // Update profile information in the UI
    const profileSection = document.getElementById("profileSection");
    if (profileSection) {
        profileSection.innerHTML = `
            <h2>Profile Information</h2>
            <p><strong>Name:</strong> ${userData.name}</p>
            <p><strong>Date of Birth:</strong> ${userData.date_of_birth}</p>
            <p><strong>Gender:</strong> ${userData.gender}</p>
            <p><strong>Phone:</strong> ${userData.phone}</p>
            <p><strong>Address:</strong> ${userData.address_line}, ${userData.city}, ${userData.state} ${userData.postal_code}</p>
            <p><strong>Blood Type:</strong> ${userData.blood_type || 'Not specified'}</p>
            <p><strong>Allergies:</strong> ${userData.allergies || 'None reported'}</p>
            <p><strong>Emergency Contact:</strong> ${userData.emergency_contact_name} (${userData.emergency_contact_relationship})</p>
        `;
    }
}

function updateMedicalRecordsTable(records) {
    const tableBody = document.getElementById("recordsTableBody");
    if (!tableBody) return;
    
    tableBody.innerHTML = "";
    records.forEach((record) => {
        const row = `
            <tr>
                <td>${record.date}</td>
                <td>${record.diagnosis}</td>
                <td>${record.treatment}</td>
                <td>${record.medication || 'N/A'}</td>
                <td>${record.doctor}</td>
                <td>${record.hospital}</td>
                <td><button onclick="deleteRecord(${record.id})">Delete</button></td>
            </tr>
        `;
        tableBody.innerHTML += row;
    });
}

// Only add event listener if the form exists
const addRecordForm = document.getElementById("addRecordForm");
if (addRecordForm) {
    addRecordForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        
        // Get the stored user data
        const userData = JSON.parse(localStorage.getItem('userData'));
        if (!userData) {
            alert('Please log in first');
            return;
        }
        
        const record = {
            pin: document.getElementById("patientPin").value.trim(),
            date: document.getElementById("date").value,
            diagnosis: document.getElementById("diagnosis").value,
            treatment: document.getElementById("treatment").value,
            medication: document.getElementById("medication").value,
            doctor: document.getElementById("doctor").value,
            hospital: document.getElementById("hospital").value,
        };
        
        try {
            const response = await fetch('/api/patient/medical-records', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify(record)
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Failed to add medical record');
            }
            
            // Refresh the profile to get updated records
            const profileResponse = await fetch('/api/patient/profile', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    pin: record.pin
                })
            });
            
            if (!profileResponse.ok) {
                throw new Error('Failed to refresh records');
            }
            
            const profileData = await profileResponse.json();
            updateMedicalRecordsTable(profileData.medical_records);
            e.target.reset();
        } catch (error) {
            console.error('Error adding medical record:', error);
            alert(error.message);
        }
    });
}

async function deleteRecord(recordId) {
    // Get the stored user data
    const userData = JSON.parse(localStorage.getItem('userData'));
    if (!userData) {
        alert('Please log in first');
        return;
    }
    
    if (!confirm('Are you sure you want to delete this record?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/patient/medical-records/${recordId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                pin: document.getElementById("patientPin").value.trim()
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to delete medical record');
        }
        
        // Refresh the profile to get updated records
        const profileResponse = await fetch('/api/patient/profile', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                pin: document.getElementById("patientPin").value.trim()
            })
        });
        
        if (!profileResponse.ok) {
            throw new Error('Failed to refresh records');
        }
        
        const profileData = await profileResponse.json();
        updateMedicalRecordsTable(profileData.medical_records);
    } catch (error) {
        console.error('Error deleting medical record:', error);
        alert(error.message);
    }
}

function navigateToAddPatient() {
    window.location.href = "add_patient.html";
}

function togglePinVisibility() {
    const pinInput = document.getElementById('patientPin');
    const toggleButton = document.querySelector('.toggle-pin-visibility i');
    
    if (pinInput.type === 'password') {
        pinInput.type = 'text';
        toggleButton.classList.remove('fa-eye');
        toggleButton.classList.add('fa-eye-slash');
    } else {
        pinInput.type = 'password';
        toggleButton.classList.remove('fa-eye-slash');
        toggleButton.classList.add('fa-eye');
    }
}

// Add input validation for PIN
document.getElementById('patientPin').addEventListener('input', function(e) {
    this.value = this.value.replace(/[^0-9]/g, '').slice(0, 6);
});