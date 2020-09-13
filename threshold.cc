#include <opencv2/opencv.hpp>

int main(int argc, char** argv) {
    char* inputFile = argv[1];
    char* outputFile = argv[2];
    
    cv::Mat wim, im = cv::imread(inputFile, cv::IMREAD_COLOR);
    cv::inRange(im, cv::Scalar(200, 200, 200), cv::Scalar(255, 255, 255), wim);

    cv::imwrite(outputFile, wim);
}