package main

import (
	"fmt"
	//"os/exec"
	//"runtime"
	//"github.com/gizak/termui/v3"
	//"github.com/gizak/termui/v3/widgets"
)

// ---- Metrics Functions ----
func getCPUTemp() string {
	// TODO Retrieve Actual Data
	return "50C"
}

func getDiskUsage() string {
	// TODO Retrieve Actual Data
	return "10MB"
}

func getMemoryUsage() string {
	// TODO Retrieve Actual Data
	return "80GB"
}

// ---- Main Program ----
func main() {
    // 1. Initialize termui
    // 2. Create widgets
    // 3. Render widgets
    // 4. Event loop

	cpuTemp := getCPUTemp()
	diskUsage := getDiskUsage()
	memoryUsage := getMemoryUsage()
	
	fmt.Printf("Current CPU Temp: %s\nCurrent Disk Usage: %s\nCurrent Memory Usage: %s\n", cpuTemp, diskUsage, memoryUsage)

}
