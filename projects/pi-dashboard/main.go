package main

import (
	"fmt"
	"log"
	"strconv"
	"strings"

	//"os/exec"
	//"runtime"
	ui "github.com/gizak/termui/v3"
	"github.com/gizak/termui/v3/widgets"
)

// ---- Metrics Functions ----
func getCPUTemp() float64 {
	// TODO Retrieve Actual Data
	tempStr := "temp=45.5'C"
	
	// Remove the prefix and suffix to get the numeric value
	tempStr = strings.TrimPrefix(tempStr, "temp=")
	tempStr = strings.TrimSuffix(tempStr, "'C")

	tempNum, err := strconv.ParseFloat(tempStr, 64)
	if err != nil {
		fmt.Println("Error converting string to integer:", err)
	}

	return tempNum
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
	
	fmt.Printf("Current CPU Temp: %f\nCurrent Disk Usage: %s\nCurrent Memory Usage: %s\n", cpuTemp, diskUsage, memoryUsage)

	// Create and Render Widgets
	if err := ui.Init(); err != nil {
		log.Fatalf("failed to initialize termui: %v", err)
	}
	defer ui.Close()


	p2 := widgets.NewPlot()
	p2.Title = "dot-mode Scatter Plot"
	p2.Marker = widgets.MarkerDot
	p2.Data = make([][]float64, 2)
	p2.Data[0] = []float64{2, 4, 8, 16, 32}
	p2.Data[1] = []float64{1, 1, 2, 3, cpuTemp}
	p2.SetRect(0, 15, 50, 30)
	p2.AxesColor = ui.ColorWhite
	p2.LineColors[0] = ui.ColorCyan
	p2.PlotType = widgets.ScatterPlot


	ui.Render(p2)

	uiEvents := ui.PollEvents()
	for {
		e := <-uiEvents
		switch e.ID {
		case "q", "<C-c>":
			return
		}
	}
}


func NewCPUWidget() *widgets.Gauge {
    g := widgets.NewGauge()
    g.Title = "CPU Usage"
    g.SetRect(0, 0, 50, 3)
    g.BarColor = ui.ColorGreen
    g.BorderStyle.Fg = ui.ColorWhite
    return g
}

func NewMemoryWidget() *widgets.Gauge {
    g := widgets.NewGauge()
    g.Title = "Memory Usage"
    g.SetRect(0, 4, 50, 7)
    g.BarColor = ui.ColorMagenta
    return g
}