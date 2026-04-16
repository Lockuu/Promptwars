package com.stadium.twin.controller;

import com.stadium.twin.model.Zone;
import com.stadium.twin.service.ZoneLogicService;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "*")
public class StadiumDataController {

    private final ZoneLogicService zoneLogicService;

    public StadiumDataController(ZoneLogicService zoneLogicService) {
        this.zoneLogicService = zoneLogicService;
    }

    @PostMapping("/sensor-update")
    public Zone updateZone(@RequestBody Zone zoneUpdate) {
        return zoneLogicService.processZoneUpdate(zoneUpdate);
    }
}
