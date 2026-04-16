// The backend STOMP endpoint
const SOCKET_URL = 'http://localhost:8081/stomp';

let stompClient = null;

function connect() {
    const socket = new SockJS(SOCKET_URL);
    stompClient = Stomp.over(socket);
    
    // Disable debug logs for cleaner console
    stompClient.debug = null;

    stompClient.connect({}, function(frame) {
        console.log('Connected: ' + frame);
        
        // Subscribe to the stadium topic
        stompClient.subscribe('/topic/stadium', function(message) {
            const zoneData = JSON.parse(message.body);
            updateZone(zoneData);
        });
    }, function(error) {
        console.error('STOMP error:', error);
        // Try to reconnect in 5 seconds
        setTimeout(connect, 5000);
    });
}

function updateZone(zone) {
    const zoneElement = document.getElementById(zone.id);
    if (!zoneElement) return;

    // Update numbers
    const countElement = zoneElement.querySelector('.count');
    // Animate count change
    animateNumber(countElement, parseInt(countElement.innerText), zone.currentCount);
    
    // Remove previous status classes
    zoneElement.classList.remove('status-green', 'status-yellow', 'status-red');
    
    // Add current status class
    const statusClass = `status-${zone.safetyStatus.toLowerCase()}`;
    zoneElement.classList.add(statusClass);
}

function animateNumber(element, start, end) {
    if (isNaN(start)) start = 0;
    if (start === end) return;
    
    let current = start;
    const diff = end - start;
    const stepTime = Math.abs(Math.floor(1000 / diff));
    const step = diff > 0 ? 1 : -1;
    
    const timer = setInterval(function() {
        current += step;
        element.innerText = current;
        if (current === end) {
            clearInterval(timer);
        }
    }, stepTime > 50 ? 50 : stepTime); // Cap the speed
}

// Ensure elements start with a default layout state
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.zone').forEach(z => z.classList.add('status-green'));
    connect();
});
