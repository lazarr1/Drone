#include <iostream>
#include <errno.h>
#include <wiringPiI2C.h>

int main(){

    int fd, result;


    fd = wiringPiI2CSetup(0x1d);

    std::cout << fd << std::endl;
    
    int j = 1;
    while(j){
        std::cout << wiringPiI2CRead(fd) << std::endl;

        std::cin >> j;
    }
}

//g++ read_imu.cpp -l wiringPi -o read