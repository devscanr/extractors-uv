from ..utils import normalize
from .phone import parse_phones

def parse(text: str) -> list[str]:
  return parse_phones(normalize(text))

# Phone numbers are fake (generated). Potential clashes will contacts
# of real people are non-intentional.

def describe_parse_phones() -> None:
  def it_parses_international() -> None:
    assert parse("+1 123 456-7890") == ["+11234567890"]  # US
    assert parse("+44 20 1234 5678") == ["+442012345678"]  # UK
    assert parse("+61 2 1234 5678") == ["+61212345678"]  # Australia
    assert parse("+1 416 123-4567") == ["+14161234567"]  # Canada
    assert parse("+39 02 1234 5678") == ["+390212345678"]  # Italy
    assert parse("+91 12345 67890") == ["+911234567890"]  # India
    assert parse("+91 1234-567890") == ["+911234567890"]  # India v2
    assert parse("+49 999 12345678") == ["+4999912345678"]  # Germany
    assert parse("+49 30 12345678") == ["+493012345678"]  # Germany v2

  def it_parses_newlined() -> None:
    assert parse("+49\n30\n12345678") == ["+493012345678"]

  def it_does_not_parse_arithmetic() -> None:
    assert parse("x = 1 + 3.14") == []
    assert parse("(17 +30658)") == []
    assert parse("49x+384") == []
    assert parse("+38,400,800$") == []
    assert parse("+38,400,800$") == []
    assert parse("0793412657 seconds elapsed") == []

  def it_parses_unicoded() -> None:
    assert parse("☎ 5573558") == ["5573558"]
    assert parse("📞5573558") == ["5573558"]
    assert parse("☎️5573558") == ["5573558"]
    assert parse("📱:5573558") == ["5573558"]

  def it_parses_urled() -> None:
    assert parse("https://wa.me/15551234567") == ["+15551234567"]
    assert parse("whatsapp: https://wa.me/+13096314912") == ["+13096314912"]
    assert parse("https://wa.me/+2347032434912") == ["+2347032434912"]
    assert parse("https://wa.me/+2347032434912?someparam") == ["+2347032434912"]
    assert parse("https://t.me/+15551234567") == ["+15551234567"]
    assert parse("https://t.me/15551234567") == ["+15551234567"]

  def it_parses_prefixed_set1() -> None:
    assert parse("Automotive developer in Reproteq & Fixhex [phone +44 637594190]") == ["+44637594190"]
    assert parse("phone: 27737526637 WeChat: 27737526367") == ["27737526637"]
    assert parse("Email: natt@gmail.com Phone: +54 7934483354 +96 13729958189") == ["+547934483354"]
    assert parse("WeChat & Phone: 28813178921. Email: zangho@lab.com") == ["28813178921"]
    assert parse("Avid Full Stack Developer Email: akashkash934@hotmail.ru Phone: +81 7355891640") == ["+817355891640"]

  def it_parses_prefixed_set2() -> None:
    assert parse("Python-backend developer Phone: +998950609954") == ["+998950609954"]
    assert parse("HCM66 Phone https://hcm66.com | https://hcm66.com | https://hcm666.com") == []
    assert parse("Phone Number: +55 91 99601-4554 E-mail: antonioluca902@gmail.com") == ["+5591996014554"]
    assert parse("Phone: +84.933911093 Email: 1870583@vermut.edu.vn / cxtinh.gov.vn") == ["+84933911093"]
    assert parse("Phone : +94 769767692 || Email : mohamedalthaff@gmail.com || Phone +555") == ["+94769767692"]

  def it_parses_prefixed_set3() -> None:
    assert parse("email: bishal-hadka-1600@gg.com phone: 970-799-9291") == ["9707999291"]
    assert parse("Consultant/Trainer - React.js, Node.js Phone:- 8637 44 8012") == ["8637448012"]
    assert parse("Phone: +380969490333") == ["+380969490333"]
    assert parse("Sefine Shipyard Phone: +90(553) 382 85 13 https://www.linkedin.com/in/hhy34/") == ["+905533828513"]
    assert parse("Email: justin.rick@gmail.com Phone: 9046571689") == ["9046571689"]

  def it_parses_prefixed_set4() -> None:
    assert parse("Django And Flutter Contributor - OpenSRP Phone: 0653188031") == ["0653188031"]
    assert parse("kakao:youngchol2 phone:010-4417-3317") == ["01044173317"]
    assert parse("I am a web developer Email : 99haroon99@gmail.com. Phone : 03122325792") == ["03122325792"]
    assert parse("QQ:3206771968 Phone-Number: 86-13979231490 Wechat:tel-F4 Add-Me") == ["8613979231490"]
    assert parse("EMAIL: otakoijairus@gmail.com | PHONE: +254722763364") == ["+254722763364"]

  def it_parses_prefixed_set5() -> None:
    assert parse("phone:93-009-1994 Front-end developer") == ["930091994"]
    assert parse("Phone : 03028921818") == ["03028921818"]
    assert parse("Phone number: 0793412657") == ["0793412657"]
    assert parse("email: huyhain926guyen@gmail.com phone: (+84) 39-226-0047") == ["+84392260047"]
    assert parse("Cell phone: 603-923-3615") == ["6039233615"]

  def it_parses_prefixed_set6() -> None:
    assert parse("QQ:308066400 Zzz:+1.2086141414 phone：+86.13516521121") == ["+8613516521121"]
    assert parse("Phone number : +964 07705856141") == ["+96407705856141"]
    assert parse("Phone number : 09078451758") == ["09078451758"]
    assert parse("phone: +86 186-4202-1059") == ["+8618642021059"]
    assert parse("Phone: 03366893938") == ["03366893938"]

  def it_parses_prefixed_set7() -> None:
    assert parse("Phone +18608000001") == ["+18608000001"]
    assert parse("Phone : 03422080317") == ["03422080317"]
    assert parse("webchat : 18210659133 phone : +8618210659133 💯") == ["+8618210659133"]
    assert parse("E-mail: ahmedalmohammed2@gmail.com Phone: +962777128689") == ["+962777128689"]
    assert parse("QQ:825846102 Phone:15910377031") == ["15910377031"]

  def it_parses_prefixed_set8() -> None:
    assert parse("Tel: +7919-086-29-27") == ["+79190862927"]
    assert parse("Phone: +7(919)-086-2977") == ["+79190862977"]
    assert parse("Phone : +989395912630") == ["+989395912630"]
    assert parse("From: Uzbekistan Phone: +998903519040") == ["+998903519040"]
    assert parse("phone/mobile = +918210268246") == ["+918210268246"]

  def it_parses_prefixed_set9() -> None:
    assert parse("Phone numbers: +1 (443) 216-1111") == ["+14432161111"]  # number(s)
    assert parse("📞 + 91 - 7680896811") == ["+917680896811"]  # space after +

  def it_parses_prefixed_set10() -> None:
    # Messengers
    assert parse("WhatsApp: +36202687810") == ["+36202687810"]
    assert parse("Viber: +36202687810") == ["+36202687810"]
    assert parse("Telegram: +36202687810") == ["+36202687810"]
    assert parse("Signal: +36202687810") == ["+36202687810"]
    assert parse("Phone/Viber/WhatsApp: +36202687812") == ["+36202687812"]
    assert parse("WhatsApp / Telegram / Signal: +1(647) 373 1111") == ["+16473731111"]
