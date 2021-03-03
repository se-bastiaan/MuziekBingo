import uuid
from django.db import models


class Player(models.Model):
    first_name1 = models.CharField(max_length=250)
    last_name1 = models.CharField(max_length=250)
    first_name2 = models.CharField(max_length=250)
    last_name2 = models.CharField(max_length=250)
    email1 = models.EmailField()
    email2 = models.EmailField()
    code = models.CharField(max_length=6)

    def user_code(self):
        return f"{self.code[0:3]}-{self.code[3:6]}"

    def __str__(self):
        return (
            f"{self.first_name1} {self.first_name2} {self.code[0:3]}-{self.code[3:6]}"
        )


class Song(models.Model):
    title = models.CharField(max_length=250)
    artist = models.CharField(max_length=250)
    played = models.BooleanField()

    def __str__(self):
        return f"{self.title} - {self.artist}"


class Card(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    item11 = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="+")
    item12 = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="+")
    item13 = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="+")
    item14 = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="+")
    item15 = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="+")
    item21 = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="+")
    item22 = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="+")
    item23 = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="+")
    item24 = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="+")
    item25 = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="+")
    item31 = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="+")
    item32 = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="+")
    item33 = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="+")
    item34 = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="+")
    item35 = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="+")
    item41 = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="+")
    item42 = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="+")
    item43 = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="+")
    item44 = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="+")
    item45 = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="+")
    item51 = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="+")
    item52 = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="+")
    item53 = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="+")
    item54 = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="+")
    item55 = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="+")

    @property
    def items(self):
        items = [list(range(5)) for _ in range(5)]

        items[0][0] = self.item11
        items[0][1] = self.item12
        items[0][2] = self.item13
        items[0][3] = self.item14
        items[0][4] = self.item15
        items[1][0] = self.item21
        items[1][1] = self.item22
        items[1][2] = self.item23
        items[1][3] = self.item24
        items[1][4] = self.item25
        items[2][0] = self.item31
        items[2][1] = self.item32
        items[2][2] = self.item33
        items[2][3] = self.item34
        items[2][4] = self.item35
        items[3][0] = self.item41
        items[3][1] = self.item42
        items[3][2] = self.item43
        items[3][3] = self.item44
        items[3][4] = self.item45
        items[4][0] = self.item51
        items[4][1] = self.item52
        items[4][2] = self.item53
        items[4][3] = self.item54
        items[4][4] = self.item55

        return items

    @items.setter
    def items(self, value):
        if len(value) < 25:
            raise Exception

        value = list(value)

        for x in range(5):
            for y in range(5):
                setattr(self, f"item{x+1}{y+1}", value.pop())
