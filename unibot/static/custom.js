// /static/custom.js

/*
 * src: https://stackoverflow.com/questions/26203453/jquery-generate-unique-ids
 */
function Generator() {};

Generator.prototype.rand =  Math.floor(Math.random() * 26) + Date.now();

Generator.prototype.getId = function() {
   return this.rand++;
};
var idGen = new Generator();

$.getScript("/static/dotdotdot.js", function() {
});
function isEmpty(obj) {
    for(var key in obj) {
        if(obj.hasOwnProperty(key))
            return true;
    }
    return false;
}

function insertLoading() {
    $( "#loading" ).remove();
    $('.chat-container').append(`
        <div class="ticontainer loading-container" id= "loading">
          <div class="tiblock">
            <div class="tidot"></div>
            <div class="tidot"></div>
            <div class="tidot"></div>
          </div>
        </div>
    `)
}

function addOptions(data, options) {
    if(data.options.length > 0) {
        $('.chat-container').append(`
            <div id="options-container">
            </div>
        `)
        for (var i = 0; i < data.options.length; i++) {
            $('#options-container').append(`
                <button class="options-button" id="option-${i}" label="option-${data.options[i]}">
                    ${data.options[i]}
                </button>
            `)
        }

        $('.options-button').on('click',function (event) {

            event.stopPropagation();
            event.stopImmediatePropagation();

            // Log the clicked element in the console
            $( "#options-container" ).remove();

            $('.chat-container').append(`
                <div class = "d-flex flex-row-reverse">
                    <div class = "chat-message human-message">
                        ${event.target.innerHTML}
                    </div>
                </div>
            `)

            // loading
            insertLoading()

            // send the message
            submit_message(event.target.innerHTML)
        });
    }
}

function scrollDown() {
    var ele = document.getElementsByClassName("chat-container")[0];
    ele.scrollTop = ele.scrollHeight;
}

function add_content_in_bubble(data,index, uid) {
    more = "<button type='button' class='btn btn-link' id= "+"more-btn-"+ uid +" >More</button>"

    first_half = data.substr(0, index+1)
    second_half = data.substr(index+1, data.length)
    id="first-content-"+uid
    append_data(first_half+more,id)
    id="second-content-"+uid
    append_data(second_half,id)
    $('#'+id).hide()
    $('#'+id).removeClass("d-flex")
    $('#'+id).removeClass("flex-row")

    $( "#" + "more-btn-" + uid ).click(function() {
        $('#'+id).addClass("d-flex")
        $('#'+id).addClass("flex-row")
        $( "#" + "second-content-" + uid ).show();
        scrollDown()
        $('#' + "more-btn-" + uid ).remove()
    });
}

function split_data(data) {
    flag = 0
    uid = idGen.getId()
    for( var index = Math.round(data.length/2); index < data.length; index++) {
        if(data[index] == '.') {
            if(data.length - index > 50) {
                add_content_in_bubble(data, index, uid)
                flag = 1
            }
            break;
        }
    }
    if (flag == 0) {
        append_data(data,idGen.getId())
        return
    }
}

function append_data(data,id) {
    $('.chat-container').append(`
        <div class = "d-flex flex-row" id = ${id}>
            <div class = "avatar-image-cropper image-container">
                <img src="/static/images/unibot.svg" alt="Avatar">
            </div>
            <div class="chat-message bot-message">
                ${data}
            </div>
        </div>
    `)
}

function submit_message(message) {
    $.post( "/send_message", {message: message}, handle_response);

    function handle_response(data) {
        // append the bot repsonse to the div
        if ( data.message.length > 200 && data.message.indexOf("href") == -1) {
            split_data(data.message)
        } else {
            append_data(data.message,idGen.getId())
        }
        scrollDown()

        if(isEmpty(data.rich_preview)){
            $('.chat-container').append(`
                    <a class="clickable-rich-container" target="_blank" href="${data.rich_preview.url}">
                    <div class="glass-box">
                        <div class = "preview-image-cropper">
                            <img src=${data.rich_preview.image} alt="website_preview">
                        </div>
                        <div class="preview-text">
                            <text class="website-preview-title">${data.rich_preview.title}</text>
                            <p class="website-preview-description" id="preview-desc">${data.rich_preview.description}</p>
                            <p class="rich-link">${data.rich_preview.url}</p>
                        </div>
                    </div>
                </a>
            `)
            let wrapper = document.querySelector( ".website-preview-description" );
            let options = {
                height: 40
            };
            new Dotdotdot( wrapper, options );
            scrollDown()
        }

        // add clickable options
        addOptions(data,event)
        scrollDown()
      // remove the loading indicator
      $( "#loading" ).remove()
    }
}



$(document).on('keypress', function(e){
    if(e.which != 13) {
      return
   }
   e.preventDefault();
   // Log the clicked element in the console
   $( "#options-container" ).remove();

    const input_message = $('#input_message').val()
    // return if the user does not enter any text
    if (!input_message) {
      return
    }

    $('.chat-container').append(`
        <div class = "d-flex flex-row-reverse">
            <div class = "chat-message human-message">
                ${input_message}
            </div>
        </div>
    `)
    // loading
    insertLoading()
    scrollDown()

    // clear the text input
    $('#input_message').val('')

    // send the message
    submit_message(input_message)
});


//Claire Wrote this code
function countCharacters(e) {
        var $input = $(this);
        var maxLetters = $input.data('max')
        var inputLength = $input.val().length
        var $output = $('+ div', this);
        $output.text((maxLetters - inputLength) + ' characters left');

        if (e.keyCode != 8 &&
            e.keyCode != 46 &&
            e.keyCode != 13 &&
            e.keyCode != 37 &&
            e.keyCode != 39 &&
            $input.val().length >= maxLetters){
            e.preventDefault();
        }
    }

$(document).on('input', '.trim_max', function(e) {
        var max = $(this).data('max');
        $(this).val($(this).val().substring(0, max));
    });

$('.char-limit').keydown(countCharacters);
$('.char-limit').keyup(countCharacters);

window.onload = function(){
    document.getElementById("hideAll").style.display = "none";
}
