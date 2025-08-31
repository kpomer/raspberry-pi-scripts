package main

import (
	"flag"
	"log"
	"time"

	//"os/exec"
	//"runtime"
	ui "github.com/gizak/termui/v3"
	"github.com/gizak/termui/v3/widgets"
	"github.com/kpomer/raspberry-pi-scripts/projects/pi-dashboard/metrics"
)

// TODO Add functions for other metrics including Time Machine information and other connected drives or devices
// It would be nice to have information about services running (ex. Tailscale, Gunicorn/Flask API service, Samba file sharing for time machine)

// ---- Main Program ----
func main() {

	// Define a flag for sample mode (-s)
	sampleData := flag.Bool("s", false, "Use sample (fake) data instead of gathering actual system metrics")
	flag.Parse()


	
	// Create and Render Widgets
	if err := ui.Init(); err != nil {
		log.Fatalf("failed to initialize termui: %v", err)
	}
	defer ui.Close()

	// Key Inputs
	k := widgets.NewParagraph()
	k.Title = "Key Input"
	k.Text = "Press [q](fg:red) or [CTRL + C](fg:red) to QUIT"
	k.SetRect(5, 35, 40, 40)
	k.BorderStyle.Bg = ui.ColorRed

	// CPU Temp
	p2 := widgets.NewPlot()
	p2.Title = "CPU Temperature ('C)"
	p2.Marker = widgets.MarkerDot
	p2.Data = make([][]float64, 1)
	p2.Data[0] = []float64{metrics.GetCPUTemp(*sampleData)}
	p2.SetRect(0, 12, 50, 30)
	p2.AxesColor = ui.ColorWhite
	p2.LineColors[0] = ui.ColorCyan
	p2.PlotType = widgets.ScatterPlot

	// Disk Usage
	table1 := widgets.NewTable()
	table1.Title = "Disk Usage"
	table1.Rows = metrics.GetDiskUsage(*sampleData)
	table1.TextStyle = ui.NewStyle(ui.ColorWhite)
	table1.SetRect(0, 0, 100, 10)


	ui.Render(k, p2, table1)

	uiEvents := ui.PollEvents()
	ticker := time.NewTicker(time.Second).C
	for {
		select {
		case e := <-uiEvents:
			switch e.ID {
			case "q", "<C-c>":
				return
			}
		case <-ticker:
			// Recalculate CPU Temp and limit display to X values
			x := 20
			p2.Data[0] = append(p2.Data[0], metrics.GetCPUTemp(*sampleData))
			if len(p2.Data[0]) > x{
				p2.Data[0] = p2.Data[0][len(p2.Data[0]) - x:]
			}
			ui.Render(k, p2, table1)
		}
}

}