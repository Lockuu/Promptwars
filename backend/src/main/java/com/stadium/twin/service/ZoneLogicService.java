package com.stadium.twin.service;

import com.stadium.twin.model.Zone;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.stereotype.Service;

@Service
public class ZoneLogicService {

    private final SimpMessagingTemplate messagingTemplate;

    public ZoneLogicService(SimpMessagingTemplate messagingTemplate) {
        this.messagingTemplate = messagingTemplate;
    }

    public Zone processZoneUpdate(Zone zone) {
        double occupancyRate = (double) zone.getCurrentCount() / zone.getCapacity();
        
        if (occupancyRate > 0.9) {
            zone.setSafetyStatus("RED");
        } else if (occupancyRate > 0.7) {
            zone.setSafetyStatus("YELLOW");
        } else {
            zone.setSafetyStatus("GREEN");
        }
        
        // Broadcast the update to the dashboard
        messagingTemplate.convertAndSend("/topic/stadium", zone);
        
        return zone;
    }
}
