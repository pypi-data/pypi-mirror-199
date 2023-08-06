# noinspection PyUnresolvedReferences
from AppKit import NSPasteboard, NSPasteboardTypeString, NSPasteboardTypeFileURL, NSPasteboardTypeURL, NSPasteboardTypeTIFF, NSArray, NSPasteboardTypeColor, NSPasteboardTypeHTML, NSData
from PIL import Image
from urllib.parse import urlparse
import io
from typing import Union


# noinspection PyUnresolvedReferences
class ClipBoard:
    encoding = "UTF-8"

    def __init__(self):
        self.clipboard = NSPasteboard.generalPasteboard()

    def copyImage(self, image: Union[Image.Image, str]) -> None:
        if isinstance(image, Image.Image):
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            self.clipboard.declareTypes_owner_(
                NSArray.arrayWithObject_(NSPasteboardTypeTIFF),
                None
            )
            self.clipboard.setData_forType_(NSData.dataWithBytes_length_(img_byte_arr.getvalue(), len(img_byte_arr.getvalue())), NSPasteboardTypeTIFF)
        elif isinstance(image, str):
            copyImage(Image.open(image))

    def copyText(self, text: str) -> None:
        self.clipboard.declareTypes_owner_(NSArray.arrayWithObject_(NSPasteboardTypeString),None)
        self.clipboard.setString_forType_(text, NSPasteboardTypeString)

    def copyFile(self, file: str) -> None:
        self.clipboard.declareTypes_owner_(NSArray.arrayWithObject_(NSPasteboardTypeFileURL),None)
        self.clipboard.setString_forType_(file, NSPasteboardTypeFileURL)

    def copyURL(self, url: str) -> None:
        try:
            urlparse(url)
        except:
            raise ValueError(url + "is not a valid URL")
        self.clipboard.declareTypes_owner_(NSArray.arrayWithObject_(NSPasteboardTypeURL),None)
        self.clipboard.setString_forType_(url, NSPasteboardTypeURL)

    def copyColor(self, color: int) -> None:
        self.clipboard.declareTypes_owner_(NSArray.arrayWithObject_(NSPasteboardTypeColor), None)
        self.clipboard.setString_forType_(str(hex(color)), NSPasteboardTypeColor)

    def copyHTML(self, html: str) -> None:
        self.clipboard.declareTypes_owner_(NSArray.arrayWithObject_(NSPasteboardTypeHTML), None)
        self.clipboard.setString_forType_(html, NSPasteboardTypeHTML)

    def get(self) -> Union[Image.Image, int, str]:
        if self.clipboard.dataForType_(NSPasteboardTypeTIFF):
            return Image.open(io.BytesIO(self.clipboard.dataForType_(NSPasteboardTypeTIFF)))
        elif self.clipboard.dataForType_(NSPasteboardTypeString):
            return self.clipboard.dataForType_(NSPasteboardTypeString).decode(self.encoding)
        elif self.clipboard.dataForType_(NSPasteboardTypeColor):
            return int(self.clipboard.stringForType_(NSPasteboardTypeColor), 16)
        elif self.clipboard.dataForType_(NSPasteboardTypeHTML):
            return self.clipboard.dataForType_(NSPasteboardTypeHTML).decode(self.encoding)
        elif self.clipboard.dataForType_(NSPasteboardTypeURL):
            return self.clipboard.dataForType_(NSPasteboardTypeURL).decode(self.encoding)
        elif self.clipboard.dataForType_(NSPasteboardTypeFileURL):
            return self.clipboard.dataForType_(NSPasteboardTypeFileURL).decode(self.encoding)


