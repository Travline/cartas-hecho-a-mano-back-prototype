from fastapi import FastAPI
from fastapi.responses import FileResponse
from dataclasses import dataclass
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from routes.auth import router as auth_router

app = FastAPI()


app.include_router(auth_router, prefix="/auth")

origins = [
    "http://localhost:4321",
    "https://cartas-hecho-a-mano-prototype.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@dataclass
class Card:
    card_id: int
    img: List[str]
    name: str
    details: str

cards: List[Card] = [
    Card(1, ["1.jpeg"], "Carta 1", "Carta a mano para tu pareja o amistades"),
    Card(2, ["2.jpeg"], "Carta 2", "Carta a mano para invitaciones de boda / aniversario."),
    Card(3, ["3.jpeg"], "Carta 3", "Carta a mano para felicitación de cumpleaños"),
    Card(4, ["4.jpeg"], "Carta 4", "Cartas a mano para felicitar a tus trabajadores"),
    Card(5, ["5.jpeg"], "Carta 5", "Cartas a mano para felicitar en Navidad & Año nuevo"),
]

@app.get("/cards")
async def get_cards():
    return cards

@app.get("/cards/img")
async def get_images():
    res: list[dict] =[]
    for card in cards:
        res.append({"img_id":card.card_id})
    return res

@app.get("/cards/img/{card_id}")
async def get_card_img(card_id: int):
    # Añadimos una validación simple para evitar errores de índice
    if card_id < 1 or card_id > len(cards):
        return {"error": "Card not found"}
    
    path = f"imgs/{cards[card_id-1].img[0]}"
    return FileResponse(path=path)