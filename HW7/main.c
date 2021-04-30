#include <xc.h>           // processor SFR definitions
#include <sys/attribs.h>  // __ISR macro
#include <stdio.h>
#include "spi.h"
#include <math.h>

#define PI acos(-1)

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


void setVoltage(char a, unsigned short v) {
    
    unsigned short r;
    unsigned char g = 1;
    unsigned char s = 1;
    unsigned char b = 1;
   
    r = (a<<15);
    r = r|(b<<14);
    r = r|(g<<13);
    r = r|(s<<12);
	r = r|((v&0b1111111111)<<2);
	
	LATAbits.LATA0 = 0;
	spi_io(r>>8);
	spi_io(r);
    LATAbits.LATA0 = 1; 
}


int main() {

    __builtin_disable_interrupts(); // disable interrupts while initializing things

    // set the CP0 CONFIG register to indicate that kseg0 is cacheable (0x3)
    __builtin_mtc0(_CP0_CONFIG, _CP0_CONFIG_SELECT, 0xa4210583);

    // 0 data RAM access wait states
    BMXCONbits.BMXWSDRM = 0x0;

    // enable multi vector interrupts
    INTCONbits.MVEC = 0x1;

    // disable JTAG to get pins back
    DDPCONbits.JTAGEN = 0;

    // do your TRIS and LAT commands here
    //set A4 as output initially low
    TRISAbits.TRISA4 = 0;
    LATAbits.LATA4 = 0;
    //set B4 as input
    TRISBbits.TRISB4 = 1;

    __builtin_enable_interrupts();
    
    initSPI();
    
    int i = 0;
    int x = 0;
    int b = 0;
    float m = 0;
    
    while(1) {
        _CP0_SET_COUNT(0);

        //make sin
        float wave = 511 + 430 * sin((2*acos(-1)*i)/100);
        i++;
        setVoltage(0, wave);
        
        //make triangle
        float y = m*x+b;
        x++;
        setVoltage(1, y);
        if(x<=100)
        {
            m = 9;
        }
        else if(x<=200)
        {
            m = -1*m;
        }
        else
        {
            x = 0;
        }
        
        while(_CP0_GET_COUNT() < 120000) 
        {
            ;
        }
    }
}