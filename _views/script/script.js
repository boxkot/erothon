$(document).ready(function(){
    to_update();
    update_button_check();
});

function update_button_check() {
    $('#update_button_check').click(function(event) {
        event.preventDefault();
        list = document.getElementsByName('update[]');
        for (i = 0; i < list.length; i++) {
            list[i].checked = true;
        }
    });
}

function to_update() {
    $('#go_update').click(function(event) {
        event.preventDefault();

        //チェックリスト取得してAjax送信
        postList = {}
        list     = ['favorite[]', 'dust[]', 'update[]']
        for (i = 0; i < list.length; i++) {
            data              = document.getElementsByName(list[i])
            postList[list[i]] = []
            for (j = 0; j < data.length; j++) {
                if (data[j].checked) {
                    postList[list[i]].push(data[j].value)
                }
            }
        }
        $.post('http://localhost/fc2/index/movie_update/',
              postList,
              function(text) {});
        alert('処理が完了しました');
    });
}

//ライトボックスっぽいもの
search = document.getElementById('_search');
if (search !== null) {
    search.onclick = function() {
        box                    = document.getElementById('_search_box');
        contents               = document.getElementById('_contents');
        close                  = document.getElementById('_close');
        box.style.display      = 'block';
        contents.style.display = 'block';
        close.onclick          = function() {
            box                    = document.getElementById('_search_box');
            contents               = document.getElementById('_contents');
            box.style.display      = 'none';
            contents.style.display = 'none';
        }
    };
}
