import time

import numpy as np
import cv2 as cv
from ctypes import windll, byref, c_ubyte
from ctypes.wintypes import RECT, HWND
import numpy as np
import win32api
import win32con
import win32gui
GetDC = windll.user32.GetDC
CreateCompatibleDC = windll.gdi32.CreateCompatibleDC
GetClientRect = windll.user32.GetClientRect
CreateCompatibleBitmap = windll.gdi32.CreateCompatibleBitmap
SelectObject = windll.gdi32.SelectObject
BitBlt = windll.gdi32.BitBlt
SRCCOPY = 0x00CC0020
GetBitmapBits = windll.gdi32.GetBitmapBits
DeleteObject = windll.gdi32.DeleteObject
ReleaseDC = windll.user32.ReleaseDC
AttachThreadInput = windll.user32.AttachThreadInput
MapVirtualKeyA = windll.user32.MapVirtualKeyA
current = win32api.GetCurrentThreadId()
# 排除缩放干扰
windll.user32.SetProcessDPIAware()

def doClick(cx, cy,hwnd):
    long_position = win32api.MAKELONG(cx, cy)  # 模拟鼠标指针 传送到指定坐标
    win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)  # 模拟鼠标按下
    time.sleep(0.1)
    win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)  # 模拟鼠标弹起
def sendKey(hwnd, key):
    """
    后台发送按键
    :param hwnd:窗口句柄
    :param key:按键值
    :return:
    """
    lparam = win32api.MAKELONG(0, MapVirtualKeyA(key, 0)) | 0x00000001
    win32gui.SendMessage(hwnd, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
    AttachThreadInput(current, hwnd, True)
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, key, lparam)
    time.sleep(0.1)
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, key, lparam | 0xC0000000)
    time.sleep(0.1)


def capture(handle: HWND):
    """窗口客户区截图

    Args:
        handle (HWND): 要截图的窗口句柄

    Returns:
        numpy.ndarray: 截图数据
    """
    # 获取窗口客户区的大小
    r = RECT()
    GetClientRect(handle, byref(r))
    width, height = r.right, r.bottom
    # 开始截图
    dc = GetDC(handle)
    cdc = CreateCompatibleDC(dc)
    bitmap = CreateCompatibleBitmap(dc, width, height)
    SelectObject(cdc, bitmap)
    BitBlt(cdc, 0, 0, width, height, dc, 0, 0, SRCCOPY)
    # 截图是BGRA排列，因此总元素个数需要乘以4
    total_bytes = width*height*4
    buffer = bytearray(total_bytes)
    byte_array = c_ubyte*total_bytes
    GetBitmapBits(bitmap, total_bytes, byte_array.from_buffer(buffer))
    DeleteObject(bitmap)
    DeleteObject(cdc)
    ReleaseDC(handle, dc)
    # 返回截图数据为numpy.ndarray
    return np.frombuffer(buffer, dtype=np.uint8).reshape(height, width, 4)
if __name__ == "__main__":
    handle = windll.user32.FindWindowW(None, "*11.txt - 记事本")

    img1 = capture(handle)
  #  cv.imshow("Capture Test", img1)
  #  cv.waitKey()
img1_gray=cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
img2=cv.imread('2.jpg')
img2_gray=cv.cvtColor(img2, cv.COLOR_BGR2GRAY)
#cv.matchTemplate(img2,img1, cv.TM_CCOEFF_NORMED)
h, w = img2.shape[:2]
# 匹配
result = cv.matchTemplate(img1_gray, img2_gray, cv.TM_CCOEFF_NORMED)

min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
#print(max_loc)
#print(min_loc)
#print(result)
#print(max_val)
#print(min_val)
# max_loc为左上角
# 右下角
right_bottom = (max_loc[0] + w, max_loc[1] + h)
# 画矩形,红色的线框出来。
#cv.rectangle(img=img1, pt1=max_loc, pt2=right_bottom, color=(0, 0, 255), thickness=3)
cv.imshow('result', img1)
cv.waitKey()
cv.destroyAllWindows()
cv.namedWindow('img', cv.WINDOW_KEEPRATIO)
print(handle)

doClick(821,522,handle)
sendKey(handle,0x20)

