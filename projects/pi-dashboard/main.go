package main

import (
	"log"
	"math/rand"
	"strings"
	"time"

	//"os/exec"
	//"runtime"
	ui "github.com/gizak/termui/v3"
	"github.com/gizak/termui/v3/widgets"
)

// ---- Metrics Functions ----
func getCPUTemp() float64 {
	// TODO Retrieve Actual Data
	// COMMAND: vcgencmd measure_temp
	// SAMPLE RESPONSE: temp=53.8'C
	// tempStr := "temp=53.8'C"
	
	// // Remove the prefix and suffix to get the numeric value
	// tempStr = strings.TrimPrefix(tempStr, "temp=")
	// tempStr = strings.TrimSuffix(tempStr, "'C")

	// tempNum, err := strconv.ParseFloat(tempStr, 64)
	// if err != nil {
	// 	fmt.Println("Error converting string to integer:", err)
	// }

	// return tempNum
	min := 40.0
	max := 80.0

	// Generate a random float in the range [40.0, 80.0)
	return min + (rand.Float64() * (max - min))
}

func getDiskUsage() [][]string {
	// TODO Retrieve Actual Data
	// COMMAND: df -h /
	// SAMPLE RESPONSE:
	// Filesystem      Size  Used Avail Use% Mounted on
	// /dev/mmcblk0p2   59G  2.6G   53G   5% /
	
	
	duStr := "Filesystem      Size  Used Avail Use% Mounted on\n/dev/mmcblk0p2   59G  2.6G   53G   5% /\n/dev/mmcblk0p8   75G  32.5G   90G   30% /mnt"
	duStr = strings.Replace(duStr, "Mounted on", "Mounted_On", -1)

	duStr_Lines := strings.Split(duStr, "\n")


	var diskUsageTable [][]string
	for _, line := range duStr_Lines {
		
		// strings.Fields() handles any amount of whitespace
		strArr := strings.Fields(line)
		if len(strArr) > 0 { // Avoid appending empty slices if a line is just whitespace
			diskUsageTable = append(diskUsageTable, strArr)
		}
	}

	return diskUsageTable

}


// ---- Main Program ----
func main() {
    // 1. Initialize termui
    // 2. Create widgets
    // 3. Render widgets
    // 4. Event loop
	
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
	p2.Data[0] = []float64{getCPUTemp()}
	p2.SetRect(0, 12, 50, 30)
	p2.AxesColor = ui.ColorWhite
	p2.LineColors[0] = ui.ColorCyan
	p2.PlotType = widgets.ScatterPlot

	// Disk Usage
	table1 := widgets.NewTable()
	table1.Title = "Disk Usage"
	table1.Rows = getDiskUsage()
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
			p2.Data[0] = append(p2.Data[0], getCPUTemp())
			if len(p2.Data[0]) > x{
				p2.Data[0] = p2.Data[0][len(p2.Data[0]) - x:]
			}
			ui.Render(k, p2, table1)
		}
}

}