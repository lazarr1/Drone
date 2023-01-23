#include <iostream>
#include <errno.h>
#include <wiringPiI2C.h>

int main(){

    int fd, result;


    fd = wiringPiI2CSetup(0x1d);

    std::cout << fd << std::endl;

    if (fd == -1){
        std::cout << "Could not read address" << std::endl;
        exit(1);
    }
    

    while(1){
        std::cout << wiringPiI2CRead(fd) << std::endl;

        std::cout << fd << std::endl;
    }
}

//g++ read_imu.cpp -l wiringPi -o read