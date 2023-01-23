#include <iostream>
#include <errno.h>
#include <wiringPiI2C.h>

int main(){

    int fd, result;


    fd = wiringPiI2CSetup(0x1d);

    std::cout << fd << endl;

    while(1){
        std::cout << wiringPiI2CRead(fd) << std::endl;
    }
}