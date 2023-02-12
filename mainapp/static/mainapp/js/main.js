// получение всех объектов с классом popup-link (popup открывается при клике на любой объект с этим классом)
const popupLinks = document.querySelectorAll('.popup-link');
// получение тега body для блокировки сколла внутри него
const body = document.querySelector('body');
// получение всех объектов с классом lock-padding
const lockPadding = document.querySelectorAll('.lock-padding');

let unlock = true; // для двойных нажатий

const timeout = 500;

if(popupLinks.length > 0) // сущестование ссылок на странице
{
   for(let i = 0; i < popupLinks.length; i++)
   {
      const popupLink = popupLinks[i];
      // привязываем событие клика
      popupLink.addEventListener("click", function (e)
      {
         // получаем имя ссылки
         const popupName = popupLink.getAttribute('href').replace('#', '');
         // получаем объекта popup
         const currentPopup = document.getElementById(popupName);
         // открываем popup с помощью ф. popupOpen
         popupOpen(currentPopup);
         // запрет на перезагрузку страницы
         e.preventDefault();
      });
   }
}

// закрытие popup 
const popupCloseIcon = document.querySelectorAll('.close-popup');
if (popupCloseIcon.length > 0) //  сущестование ссылок на странице
{
   for (let i = 0; i < popupCloseIcon.length; i++)
   {
      const el = popupCloseIcon[i];
       // привязываем событие клика
      el.addEventListener("click", function (e)
      {
         // отправляем popupClose объект
         // который является ближайшим родителем с классом popup
         // при клике скрип наверху будет искать объект с классом popup и его закроет
         popupClose(el.closest('.popup'));
         e.preventDefault();
      });
   }
}

function popupOpen(currentPopup)
{
   // проверка на существование объекта
   if (currentPopup && unlock)
   {
      // получаем открытый popup
      const popupActive = document.querySelector('.popup.open');
      // при его существовании сразу закрываем его
      if (popupActive)
      {
         popupClose(popupActive, false);
      }
      else
      {
         bodyLock();
      }
      // добавляем класс open (css popup.open)
      currentPopup.classList.add('open');
      // связываем с событием click
      // отсекаем всё, кроме темной области
      currentPopup.addEventListener("click", function (e)
      {
         // т.е. закрытие при нажамии по темной области
         // если у нажатого объекта нет в родителях объекта с классом popup__content
         // то ничего не произойдет (при нажатии в области контента внутри popup)
         if (!e.target.closest('.popup__content'))
         {
            popupClose(e.target.closest('.popup'));
         }
      });
   }
}

// doUnclock - использование блокирования скролла
// открытие popup при уже открытом popup (не нужно открывать второй скролл)
function popupClose(popupActive, doUnlock = true)
{
   if (unlock)
   {
      popupActive.classList.remove('open');
      if (doUnlock)
      {
         bodyUnlock();
      }
   }
}

function bodyLock()
{
   // высчитываем разницу между шириной окна и wrapper (ширина скрола)
   const lockPaddingValue = window.innerWidth - document.querySelector('.wrapper').offsetWidth + 'px';

   // проверка на существование данных объектов
   if (lockPadding.length > 0)
   {
      // сдвиг шапки (к примеру)
      for (let i = 0; i < lockPadding.length; i++)
      {
         const el = lockPadding[i];
         el.style.paddingRight = lockPaddingValue;
      }
   }
   // присваиваем данное значение в виде padding справа
   body.style.paddingRight = lockPaddingValue;
   // присваиваем данное значение самому body (по нему убирается скролл)
   body.classList.add('lock');

   // блокировка быстрого повторого клика
   unlock = false;
   setTimeout(function ()
   {
      unlock = true;
   }, timeout);
}

function bodyUnlock()
{
   // плавное появление скролла
   setTimeout(function ()
   {
      if (lockPadding.length > 0)
      {
         // убираем padding у объектов
         for (let i = 0; i < lockPadding.length; i++)
         {
            const el = lockPadding[i];
            el.style.paddingRight = '0px';
         }
      }
      body.style.paddingRight = '0px';
      body.classList.remove('lock');
   }, timeout);
   
   unlock = false;
   setTimeout(function ()
   {
      unlock = true;
   }, timeout);
}

// закрытие popup по esc
document.addEventListener('keydown', function (e)
{
   if(e.which === 27)
   {
      const popupActive = document.querySelector('.popup.open');
      popupClose(popupActive);
   }
});


// ajax
function getCookie(name) {
   let cookieValue = null;
   if (document.cookie && document.cookie !== '') {
       const cookies = document.cookie.split(';');
       for (let i = 0; i < cookies.length; i++) {
           const cookie = cookies[i].trim();
           // Does this cookie string begin with the name we want?
           if (cookie.substring(0, name.length + 1) === (name + '=')) {
               cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
               break;
           }
       }
   }
   return cookieValue;
}

$(function ($){
   $('#logform').submit(function (e) {
      e.preventDefault()
      $.ajax({
         type: this.method,
         url: this.action,
         data: $(this).serialize(),
         headers: {'X-CSRFToken': getCookie('csrftoken')},
         dataType: 'json',
         success: function (response) {
            console.log('okay', response)
            window.location.reload();
         },
         error: function (response) {
            //console.log('err - ', response);

            var data = JSON.parse(JSON.stringify(response['responseJSON']));
            $.each(data['errors'], function( key, value ) {
               $("#response2").text( value ).append().fadeIn();
           });
         }
      })
   })
})

$(function ($){
   $('#regform').submit(function (e) {
      e.preventDefault()
      $.ajax({
         type: this.method,
         url: this.action,
         data: $(this).serialize(),
         headers: {'X-CSRFToken': getCookie('csrftoken')},
         dataType: 'json',
         success: function (response) {
            //console.log('okay', response)
            //window.location.reload();
            const curPopup = document.getElementById('popup_s');
            popupOpen(curPopup);

            setTimeout(function(){
               window.location.reload(1);
            }, 5000);

         },
         error: function (response) {
            console.log('err - ', response);
            // var data = JSON.parse(JSON.stringify(response['responseJSON']));
            // for (const [key, value] of Object.entries(data['errors'])) {
            //    $("#response").replaceWith(value);
            // }
            var data = JSON.parse(JSON.stringify(response['responseJSON']));
            $.each(data['errors'], function( key, value ) {
               $("#response").text(value).append().fadeIn();
           });
         }
      })
   })
})

$(function ($){
   $('#resetform').submit(function (e) {
      e.preventDefault()
      $.ajax({
         type: this.method,
         url: this.action,
         data: $(this).serialize(),
         headers: {'X-CSRFToken': getCookie('csrftoken')},
         dataType: 'json',
         success: function (response) {
            const curPopup = document.getElementById('popup_o');
            popupOpen(curPopup);
         },
         error: function (response) {
            console.log('err - ', response);
            var data = JSON.parse(JSON.stringify(response['responseJSON']));
            $.each(data['errors'], function( key, value ) {
               $("#response3").text(value).append().fadeIn();
           });
         }
      })
   })
})

$(function ($){
   $('#resetform2').submit(function (e) {
      e.preventDefault()
      $.ajax({
         type: this.method,
         url: this.action,
         data: $(this).serialize(),
         headers: {'X-CSRFToken': getCookie('csrftoken')},
         dataType: 'json',
         success: function (response) {
            console.log('okay', response)
         },
         error: function (response) {
            var data = JSON.parse(JSON.stringify(response['responseJSON']));
            $.each(data['errors'], function( key, value ) {
               $("#response4").text( value ).append().fadeIn();
           });
         }
      })
   })
})

// comment form
function openForm(com_id) {
   console.log("myForm_"+com_id)
   document.getElementById("myForm_"+com_id).style.display = "block";
}
 
 function closeForm(com_id) {
   document.getElementById("myForm_"+com_id).style.display = "none";
}