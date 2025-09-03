from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()
from os import getenv
client = InferenceClient(
    provider="hf-inference",
    api_key=getenv("HF_API_KEY"),
)

result = client.text_classification(
    text="""
    Title: Thoughts on DEF Corp After Recent News – Should We Be Worried or Excited?
Hey everyone,
I’ve seen a lot of discussion lately about DEF Corp, especially after their recent product announcement and the dip in share price. I wanted to throw in my two cents and see what the community thinks, since I know a lot of us are either holding or considering a position.
First off, the product launch last week definitely got people talking. The new DEF Home device looks cool, and the demo was pretty slick, but I’m not sure it’s the game-changer some are hyping it up to be. The tech seems solid, but the market is crowded, and I’m a little skeptical about how much market share DEF can realistically grab from established players. That said, I do like that they’re innovating and not just sitting on their hands.
Financials are a mixed bag. Last quarter’s revenue was up 8% year-over-year, which is decent, but profit margins are getting squeezed. Management blamed higher input costs and some supply chain headaches, which isn’t unique to DEF, but it’s still something to watch. On the plus side, they haven’t taken on much new debt, and cash flow is still positive, so I’m not panicking.
One thing that has me a bit concerned is the recent executive turnover. The CFO stepping down right after earnings isn’t a great look, and the official explanation was pretty vague. I’d love to hear if anyone has more insight on that. Sometimes it’s just routine, but sometimes it’s a red flag.
On the other hand, I do think the company’s long-term prospects are still solid. They’ve got a loyal customer base, and their R&D spending shows they’re serious about staying competitive. I also noticed a couple of analysts upgraded the stock after the product launch, which is encouraging, though price targets are all over the place.
The stock price has been choppy. It dropped about 7% after earnings, but seems to be stabilizing now. I’m guessing a lot of that is just market jitters and people reacting to headlines. For now, I’m holding my shares. I don’t see a reason to sell, but I’m also not rushing to buy more until I see how the next quarter plays out.
    """,
    model="ProsusAI/finbert",
)

print(result)