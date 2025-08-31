package metrics

import "math/rand/v2"

func GetCPUTemp(sampleData bool) float64 {

	if sampleData {
		// return sample data
		return getSampleCPUTemp()
	}

	
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
	min := 80.0
	max := 120.0

	// Generate a random float in the range [40.0, 80.0)
	return min + (rand.Float64() * (max - min))
}


func getSampleCPUTemp() float64 {

	min := 40.0
	max := 90.0

	// Generate a random float in the range [40.0, 90.0)
	return min + (rand.Float64() * (max - min))

}