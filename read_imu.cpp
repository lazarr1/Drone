#include <iostream>
#include <errno.h>
#include <wiringPiI2C.h>

int main(){

    int fd, result;


    fd = wiringPiI2CSetup(0x1d);

    std::cout << fd << std::endl;
    
    int j = 99999999;
    while(j){
        std::cout << wiringPiI2CRead(fd) << std::endl;



        if(j == 1)
            j = 9999999;
            std::cin >> j;

        j--;
    }
}

//g++ read_imu.cpp -l wiringPi -o read