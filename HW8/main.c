#include <xc.h>           // processor SFR definitions
#include <sys/attribs.h>  // __ISR macro
#include <stdio.h>
#include "i2c_master_noint.h"

// DEVCFG0
#pragma config DEBUG = OFF // disable debugging
#pragma config JTAGEN = OFF // disable jtag
#pragma config ICESEL = ICS_PGx1 // use PGED1 and PGEC1
#pragma config PWP = OFF // disable flash write protect
#pragma config BWP = OFF // disable boot write protect
#pragma config CP = OFF // disable code protect

// DEVCFG1
#pragma config FNOSC = FRCPLL // use internal oscillator with pll
#pragma config FSOSCEN = OFF // disable secondary oscillator
#pragma config IESO = OFF // disable switching clocks
#pragma config POSCMOD = OFF // internal RC
#pragma config OSCIOFNC = OFF // disable clock output
#pragma config FPBDIV = DIV_1 // divide sysclk freq by 1 for peripheral bus clock
#pragma config FCKSM = CSDCMD // disable clock switch and FSCM
#pragma config WDTPS = PS1048576 // use largest wdt
#pragma config WINDIS = OFF // use non-window mode wdt
#pragma config FWDTEN = OFF // wdt disabled
#pragma config FWDTWINSZ = WINSZ_25 // wdt window at 25%

// DEVCFG2 - get the sysclk clock to 48MHz from the 8MHz crystal
#pragma config FPLLIDIV = DIV_2 // divide input clock to be in range 4-5MHz
#pragma config FPLLMUL = MUL_24 // multiply clock after FPLLIDIV
#pragma config FPLLODIV = DIV_2 // divide clock after FPLLMUL to get 48MHz

// DEVCFG3
#pragma config USERID = 00000000 // some 16bit userid, doesn't matter what
#pragma config PMDL1WAY = OFF // allow multiple reconfigurations
#pragma config IOL1WAY = OFF // allow multiple reconfigurations

void setPin(unsigned char address, unsigned char reg, unsigned char value);  // address, register, value
char readPin(unsigned char address,unsigned char reg);           // address, register

void setPin(unsigned char address, unsigned char reg, unsigned char value)
{
    
    i2c_master_start();
    i2c_master_send(address);       //address with write bit
    i2c_master_send(reg);           //register to change
    i2c_master_send(value);         //value for change
    i2c_master_stop(); 
}

char readPin(unsigned char address, unsigned char reg)
{
    
    i2c_master_start();
    i2c_master_send(address|0);     // address with write bit
    i2c_master_send(reg);           // register to read
    i2c_master_restart();           // restart
    i2c_master_send(address|0x1);   // address with read bit
    char data = i2c_master_recv();  // receive data
    i2c_master_ack(1);              // acknowledge bit
    i2c_master_stop();
    
    return data;
}


int main()
{

    __builtin_disable_interrupts(); // disable interrupts while initializing things

    // set the CP0 CONFIG register to indicate that kseg0 is cacheable (0x3)
    __builtin_mtc0(_CP0_CONFIG, _CP0_CONFIG_SELECT, 0xa4210583);

    // 0 data RAM access wait states
    BMXCONbits.BMXWSDRM = 0x0;

    // enable multi vector interrupts
    INTCONbits.MVEC = 0x1;

    // disable JTAG to get pins back
    DDPCONbits.JTAGEN = 0;

    //set A4 as output, low
    TRISAbits.TRISA4 = 0;
    LATAbits.LATA4 = 0;
    
    //set B4 as input
    TRISBbits.TRISB4 = 1;
    
    i2c_master_setup();
    
    __builtin_enable_interrupts();

    unsigned char slave_address = 0x40;
    unsigned char button_pin = 0x13;        // GPIOB
    unsigned char led_pin = 0x14;           // OLATA
    unsigned char high = 0xFF;
    unsigned char low = 0x00;
    unsigned char button_status;                   

    while(1)
    {
        
        // Heartbeat 5Hz
        _CP0_SET_COUNT(0);
        LATAbits.LATA4 = !LATAbits.LATA4;
        while(_CP0_GET_COUNT() < 4800000){;}
        
        //LED Toggle
        button_status = readPin(slave_address, button_pin); //check for button press
        if(button_status)
        {
            
            setPin(slave_address, led_pin, low);            //turn off LED
        }
        else
        {
            setPin(slave_address, led_pin, high);           //turn on LED
        }
        
    }
}