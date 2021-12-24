if self.jumpcount >= -10:
    neg = 1
    if self.jumpcount < 0:
        neg = -1
    self.rect.bottom -= int((self.jumpcount**2) * 0.5 * neg) #replace 0.5(default) for change in height that is desired.
    self.jumpcount -= 1
else:
    self.jumpint = False
    self.jumpcount = 10
