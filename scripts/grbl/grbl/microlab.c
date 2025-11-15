#include "grbl.h"

volatile uint8_t* output_ddr[OUTPUT_MAX_NUM] = {
    &OUTPUT1_DDR,
    &OUTPUT2_DDR,
    &OUTPUT3_DDR,
    &OUTPUT4_DDR,
    &OUTPUT5_DDR
  };

  volatile uint8_t* output_port[OUTPUT_MAX_NUM] = {
    &OUTPUT1_PORT,
    &OUTPUT2_PORT,
    &OUTPUT3_PORT,
    &OUTPUT4_PORT,
    &OUTPUT5_PORT
  };

 uint8_t output_bit[OUTPUT_MAX_NUM] = {
    OUTPUT1_BIT,
    OUTPUT2_BIT,
    OUTPUT3_BIT,
    OUTPUT4_BIT,
    OUTPUT5_BIT
  };

void microlab_gpio_init(){
    
    for(uint8_t i;i< OUTPUT_MAX_NUM;i++){
        *output_ddr[i] |= (1 << output_bit[i]);
        // default output state is low
        *output_port[i] &= ~(1 << output_bit[i]);
    }

}

void microlab_set_output(uint8_t port_num, uint8_t state){

    if(port_num > OUTPUT_MAX_NUM)
        return;

    if(state)
        *output_port[port_num] |= (1 << output_bit[port_num]);
    else
         *output_port[port_num] &= ~(1 << output_bit[port_num]);
}