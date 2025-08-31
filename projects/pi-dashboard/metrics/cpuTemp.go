package metrics

import (
	"fmt"
	"math/rand"
	"os/exec"
	"strconv"
	"strings"
)

func GetCPUTemp(sampleData bool) float64 {

	var val_Str string
	if sampleData {
		// return sample data
		val_Str = getSampleCPUTemp()
	} else {
		// cmd: vcgencmd measure_temp
		cmdOutput, err := exec.Command("vcgencmd", "measure_temp").Output()
        if err != nil {
            fmt.Println("Error running command:", err)
			val_Str = ""
        } else {
			val_Str = strings.TrimSpace(string(cmdOutput)) // convert []byte to string
		}
	}

	val_Str = strings.TrimPrefix(val_Str, "temp=")
	val_Str = strings.TrimSuffix(val_Str, "'C")

	tempNum, err := strconv.ParseFloat(val_Str, 64)
	if err != nil {
		fmt.Println("Error converting string to integer:", err)
	}

	return tempNum

}


func getSampleCPUTemp() string {

	min := 40.0
	max := 90.0

	// example format: temp=57.1'C
	// Generate a random float in the range [40.0, 90.0)
	sampleCPUTemp := fmt.Sprintf("temp=%.1f'C", min + (rand.Float64() * (max - min)))

	return sampleCPUTemp

}