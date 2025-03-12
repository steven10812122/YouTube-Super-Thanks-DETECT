# YouTube Super Thanks DETECT

## Description
This project estimates the "Super Thanks" amount under YouTube videos using Python and Selenium. It automates the process of fetching data related to YouTube's "Super Thanks" feature and provides an estimated value. However, there is a bug when the number of comments is very large (e.g., several thousand). In such cases, the script may terminate unexpectedly due to an inability to process all the comments. This issue is still under investigation.


## Installation
1. Install dependencies:
   ```bash
   pip install selenium
   pip install webdriver_manager

2.Download ChromeDriver which can be searched on google and place it in the same directory as the script, or specify the path to chrome-driver.exe.

##Usage
Run the script to start detecting the "Super Thanks" amount under a YouTube video.
1.find the line : VIDEO_URL =" ", and switch " url "  to your yt url link.
2. run the python code.
3. wait for the result.

##Contributing
1. Fork this repository.
2. Create a new branch (git checkout -b feature-branch).
3. Commit your changes (git commit -am 'Add new feature').
4. Push to the branch (git push origin feature-branch).
5. Submit a pull request.

##License
The MIT License (MIT)
Copyright (c) 2025 Chun-Yen Tsai

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following condition:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
