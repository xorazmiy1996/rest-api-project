
<center>
<h1>Rest-api-project</h1>
</center>


<table>
  <tr>
    <td><img src="static/images/my_image.jpg" style="border-radius: 50%;" alt="Rasm" width="300"/></td>
    <td>
      <h3>Ibragimov Muhammad</h3>
       <ul>
         <li>Loyihani python  dasturlashni elementar(junior) biladigan  dastruchilar uchun tavsiya etaman.</li>
         <li>Ushbu loyiha orqali siz Python, Flask va mashhur kengaytmalar yordamida resursga asoslangan, ishlab chiqarishga tayyor REST API-larini yaratishga yo'l-yo'riq beradi. </li>
      </ul> 
    </td>
  </tr>
</table>


### Siz nimani o'rganasiz:

> Salom mening ismim __Muhammad__ va men Python dastrulsh mutaxassisiman. Rest-api-project loyihamda siz foydalanuvchilarni xavfsiz roʻyxatdan oʻtkazish va autentifikatsiya qilish bilan shugʻullanasiz, maʼlumotlar bazasini samarali boshqarish uchun SQLAlchemy-dan foydalanasiz va joylashtirishning murakkabliklarini oʻrganasiz.Maʼlumotlar bazasini koʻchirish uchun Git va Alembic kabi muhim texnologiyalarni qamrab olgan holda siz Python, Flask va Docker yordamida veb va REST API ishlab chiqish koʻnikmalaringizni oshirib, mijozlar autentifikatsiyasi va maʼlumotlarni boshqarish uchun REST API ishlab chiqasiz. SQLAlchemy bilan CRUD operatsiyalarini amalga oshirishni, JWT autentifikatsiyasi bilan xavfsiz API-larni, Flask-JWT-Extended yordamida foydalanuvchi autentifikatsiyasini boshqarishni, Docker va Render.com yordamida ilovalarni joylashtirishni, rq va Mailjet yordamida fon vazifalari va elektron pochta xabarlarini boshqarishni o'rganasiz.

### Loyihamizning Umumiy Biznes Logikasi:

>Har bir do'kon bir yoki bir nechta mahsulotlarni saqlaydi va har bir mahsulot teglar bilan bog'lanishi mumkin. Bu bog'lanishlar xaridorlarga mahsulotlarni qidirishda va tanlashda yordam beradi.

<ol>
    <li>Store (Do'kon)
        <ul>
            <li>Har bir do'kon o'z mahsulotlarini (items) saqlaydi.</li>
            <li>Do'konlar o'rtasida mahsulotlar almashinuvi yoki bir xil mahsulotlar bo'lishi mumkin.</li>
            <li>Do'konlar o'zlarining xaridorlariga xizmat ko'rsatadi va mahsulotlar orqali daromad olishadi.</li>
        </ul>
    </li>
    <li>Item (Mahsulot)
        <ul>
            <li>Mahsulotlar do'konlar ichida joylashgan va har bir mahsulot o'z narxi va tavsifi bilan xaridorlarga taqdim etiladi.</li>
            <li>Mahsulotlar do'konlar o'rtasida farq qiladi, ya'ni bir do'konda mavjud bo'lgan mahsulot boshqa do'konda bo'lmasligi mumkin.</li>
            <li>Mahsulotlar xaridorlar tomonidan sotib olinadi va bu do'konning daromadini oshiradi.</li>
        </ul>
    </li>
    <li>Tag (Teg)
        <ul>
             <li>Teglar mahsulotlarga qo'shiladi va ularni turli kategoriyalarga ajratadi (masalan, "ofis", "texnika", "mebel").</li>   
             <li>Teglar yordamida xaridorlar o'zlariga kerakli mahsulotlarni tezda topishlari mumkin.</li>   
             <li>Teglar do'konlar o'rtasida bir xil bo'lishi mumkin, lekin har bir do'konda o'ziga xos teglar ham bo'lishi mumkin.</li>   
        </ul>
    </li>
</ol>


### Loyihamizning SQL Struktura::

[Ushbu silka orqali ko'rishingiz mumkin](https://dbdiagram.io/d/67d6e95075d75cc844425869)
![Rasm tavsifi](static/images/model_connection_sql.png)
### Bu loyihamiz orqali biz quydagi kutobxonalr nima uchun kerak va undan foydalnish yo'llarini o'rganamiz
<table>
  <tr>
    <td>1. Flask</td>
    <td>8. Flask-migrate</td>
  </tr>
  <tr>
    <td>2. Flask-smorest</td>
    <td>9. Gunicorn </td>
  </tr>
  <tr>
    <td>3. Python-dotenv</td>
    <td>10. Psycopg2 </td>
  </tr>
  <tr>
    <td>4. Sqlalchemy</td>
    <td>11. Requests </td>
  </tr>
  <tr>
    <td>4. Flask-sqlalchemy</td>
    <td>12. Mailjet_rest </td>
  </tr>
  <tr>
    <td>5. Passlib</td>
    <td>13.  rq</td>
  </tr>
  <tr>
    <td>6. Flask-jwt-extended</td>
    <td></td>
  </tr>
</table>


### Loyihamizga docker va docker-compose fayllarini qo'shamiz.

> Docker va Docker-compose fayllari yordamida windows, linux va unix operatsion tizimlarida loyihamizni bita buyruq yordamida ishga tushurishni o'rganamiz

### Github bilan ishlashda quydagi git buyruqlarini o'rganamiz:
<table>
  <tr>
    <td>1. git init</td>
    <td>7. git pull</td>
  </tr>
  <tr>
    <td>2. git clone ...</td>
    <td>8.  git merge </td>
  </tr>
  <tr>
    <td>3. git status </td>
    <td>9. git stash </td>
  </tr>
  <tr>
    <td>4. git stash list</td>
    <td>10. git apply</td>
  </tr>
  <tr>
    <td>5. git commit -m"..."</td>
    <td>11. git branch </td>
  </tr>
  <tr>
    <td>6. git push </td>
    <td>12. git checkout</td>
  </tr>
</table>

- [Loyihamizning github dagi mazili](https://github.com/PacktPublishing/REST-APIs-with-Flask-and-Python-in-2023)

### Atrof muxit o'zgaruvchilarni boshqarishni o'rganamiz:
> .env faylini qanday ishlatishni o'rganamiz

### Mailjet bilan integratsiya qilamiz
> Foydalanuvchilar pochtasiga habar yuboramiz: [Mailjet](https://www.mailjet.com/) orqali

### Loyihaga Swagger-ui hujjatlarini qo'shishni ko'rib chiqamiz:

[Swagger-ui](https://test-uchun.uz/swagger-ui)

![Rasm tavsifi](static/images/swagger.png)

### API endPoit lari uchun  response va require uchun validatsiyalr yozamiz:

> @blue.arguments() va  @blue.response() dekoratorlari va Schema(Sxema) tushunchasini qo'llashni o'rganamiz 

### Loyihamiz uchun Unittest yozamiz:

>API'lar uchun unit testlar, API'lar orqali bajariladigan funksiyalarni alohida tekshirishga mo'ljallangan testlardir. Bu testlar API'ning har bir endpoint'ini, uning kirish va chiqish parametrlarini, va kutilgan natijalarni tekshirishda yordam beradi.


### Render.com sayti bilan tanishamiz:

> [render.com](https://render.com/) Bu sayt orqali loyihamizni serverga yuklaymiz.

### Eng so'ngida miskroservislar bilan tanishamiz
> Mikroservislar — bu dasturiy ta'minotni arxitektura uslubi bo'lib, u katta va murakkab tizimlarni kichik, mustaqil va o'zaro bog'liq xizmatlarga bo'lishni nazarda tutadi. Har bir mikroservis o'z vazifalarini bajaradi va o'zining alohida kod bazasiga, ma'lumotlar bazasiga va joylashuviga ega bo'lishi mumkin.