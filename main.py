from fastapi import FastAPI
from fastapi.responses import FileResponse
from dataclasses import dataclass

app = FastAPI()

@dataclass
class Card:
  card_id: int
  img: list[str]
  name: str
  details: str

cards: list[Card] = [
  Card("1", ["1.jpeg"], "Carta 1", "Carta a mano para tu pareja o amistades"),
  Card("2", ["2.jpeg"], "Carta 2", "Carta a mano para invitaciones de boda / aniversario."),
  Card("3", ["3.jpeg"], "Carta 3", "Carta a mano para felicitación de cumpleaños"),
  Card("4", ["4.jpeg"], "Carta 4", "Cartas a mano para felicitar a tus trabajadores"),
  Card("5", ["5.jpeg"], "Carta 5", "Cartas a mano para felicitar en Navidad & Año nuevo"),
]

@app.get("/cards")
async def get_cards():
  return cards

@app.get("/cards/img/{card_id}")
async def get_card_img(card_id:int):
  return FileResponse(path=f"imgs/{cards[card_id-1].img[0]}")