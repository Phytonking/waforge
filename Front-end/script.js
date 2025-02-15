function generateItinerary() {
    const destination = document.getElementById("destination").value;
    const startDate = document.getElementById("start-date").value;
    const endDate = document.getElementById("end-date").value;
    const itineraryList = document.getElementById("itinerary-list");
    const culturalInfo = document.getElementById("cultural-info");
    const localInfo = document.getElementById("local-info");
    
    if (!destination || !startDate || !endDate) {
        alert("Please fill in all fields.");
        return;
    }
    
    itineraryList.innerHTML = `
        <li><strong>Destination:</strong> ${destination}</li>
        <li><strong>Start Date:</strong> ${startDate}</li>
        <li><strong>End Date:</strong> ${endDate}</li>
    `;
    
    culturalInfo.textContent = `Cultural tips for ${destination}: Be respectful of local customs and dress codes.`;
    localInfo.textContent = `Local-first guide for ${destination}: Explore lesser-known attractions and support local businesses.`;
}
