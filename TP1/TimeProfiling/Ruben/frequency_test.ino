//  Available CPU clock frequency values:
//  240, 160, 80    <<< For all XTAL types
//  40, 20, 10      <<< For 40MHz XTAL
//  26, 13          <<< For 26MHz XTAL
//  24, 12          <<< For 24MHz XTAL

// Definitions
#define LED_BUILTIN 2     // Led on ESP32 board
#define DELAY 1e6         // 'for' delay amount
#define FREQUENCY 160     // CPU frequency

int xtal_freq;
int cpu_freq;
int num = 0;

void setup() {
  int n_cycles;
  float exec_time;

  // Setup
  Serial.begin(115200);           // Serial baudrate
  pinMode(LED_BUILTIN, OUTPUT);   // Set pin as output
  setCpuFrequencyMhz(FREQUENCY);  // Set desired CPU clock

  // Get crystal and CPU frequencies
  xtal_freq = getXtalFrequencyMhz();
  cpu_freq = getCpuFrequencyMhz();

  Serial.printf("XTAL Frequency = %d MHz\n", xtal_freq);
  Serial.printf("CPU Frequency = %d MHz\n", cpu_freq);

  // Start timing
  int n_i = xthal_get_ccount();

  // Begin program
  for(int i = 0; i < DELAY; i++){
    num++;
  }

  // End timing
  int n_f = xthal_get_ccount();

  // Calculate CPU cycles
  n_cycles = n_f - n_i;
  // Calculate execution time
  exec_time = float(n_cycles) / float(cpu_freq) * 1000.0;

  // Display
  Serial.printf("Execution clock cycles = %d\n", n_cycles);
  Serial.printf("Execution time = %.2f ns\n", exec_time);
}

void loop() {
  // Nothing to loop
}
