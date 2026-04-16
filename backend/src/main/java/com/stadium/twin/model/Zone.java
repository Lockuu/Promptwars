package com.stadium.twin.model;

public class Zone {
    private String id;
    private String name;
    private int currentCount;
    private int capacity;
    private String safetyStatus;

    public Zone() {}

    public Zone(String id, String name, int currentCount, int capacity, String safetyStatus) {
        this.id = id;
        this.name = name;
        this.currentCount = currentCount;
        this.capacity = capacity;
        this.safetyStatus = safetyStatus;
    }

    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public int getCurrentCount() { return currentCount; }
    public void setCurrentCount(int currentCount) { this.currentCount = currentCount; }

    public int getCapacity() { return capacity; }
    public void setCapacity(int capacity) { this.capacity = capacity; }

    public String getSafetyStatus() { return safetyStatus; }
    public void setSafetyStatus(String safetyStatus) { this.safetyStatus = safetyStatus; }
}
