#include<xc.h>           // processor SFR definitions
#include<sys/attribs.h>  // __ISR macro
#include <stdio.h>
#include "spi.h"
#include "font.h"
#include "ST7789.h"

#define IMU_WHOAMI 0x0f
#define IMU_OUT_TEMP_L 0x20
#define IMU_CTRL1_XL 0x10
#define IMU_CTRL2_G 0x11
#define IMU_CTRL3_C 0x12
#define IMU_CTRL3_C 0x12

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

void drawLevel(int x, int y);

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

    TRISAbits.TRISA4 = 0;
    LATAbits.LATA4 = 1;
    
    i2c_master_setup();
    writePin(IMU_CTRL1_XL,0b10000010); // set accel rate to 1.66 kHz, 2g sensitivity, 100hz filter
    writePin(IMU_CTRL2_G,0b10001000); //set gyro rate to 1.66 kHz, 1000 dps
    writePin(IMU_CTRL3_C,0b00000100); //enable IF_INC
    
    initSPI();
    LCD_init();
    //imu_setup();
    __builtin_enable_interrupts();
    
    int x;
    int y;
    unsigned char data[14];
    LCD_clearScreen(BLACK);
    
    while (1)
    {
        _CP0_SET_COUNT(0);
        I2C_read_multiple(IMU_OUT_TEMP_L,data,14);
        
        signed short a_x = data[9]<<8 | data[8];
        signed short a_y = data[11]<<8 | data[10];

        y = -0.0075*a_x+120;
        x = -0.0075*a_y+120;    
        
        drawLevel(x,y);
    }

}

void drawLevel(int x, int y)
{
    int pix;
    int i;
    
    if(x>120)
    {
        for(i=120;i<x;i++)
        {
            for(pix=119;pix<122;pix++)
            {
                LCD_drawPixel(i,pix,WHITE);
            }
        }
    }
    else
    {
        for(i=x;i<120;i++)
        {
            for(pix=119;pix<122;pix++)
            {
                LCD_drawPixel(i,pix,WHITE);
            }
        }
    }
    if(y>120)
    {
        for(i=120;i<y;i++)
        {
            for(pix=119;pix<122;pix++)
            {
                LCD_drawPixel(pix,i,BLUE);
            }
        }
    }
    else
    {
        for(i=y;i<120;i++)
        {
            for(pix=119;pix<122;pix++)
            {
                LCD_drawPixel(pix,i,BLUE);
            }
        }
    }
    for(x = 119;x<122;x++)
    {
        for(y = 0;y<241;y++)
        {
            LCD_drawPixel(x,y,BLACK);
        }
    }
    for(x = 0;x<241;x++)
    {
        for(y = 119;y<122;y++)
        {
            LCD_drawPixel(x,y,BLACK);
        }
    }
}

