// 구현정 댓글 작업 중==============================================================
// 댓글 삭제는 어떻게 하는가...
function del(){
    $('.post-comment').hide()
}

function show_comment() {
    $.ajax({
        type: 'GET',
        url: '/comment',
        data: {},
        success: function (response) {
                let rows = response['comment']
                for (let i = 0; i < rows.length; i++) {
                    // let user_name = rows[i]['user_name']
                    let comment = rows[i]['comment']
                    //let post_num = rows[i]['post_num']
                    //${post_num}
                    let temp_html = `<div class="post-comment">
                                      <p class="post-author">나는냐댓글닝겐:</p><p>${comment}</p>
                                      <p class="comment-btn" onclick="del()">삭제</p>
                                      </div>`

                    $('#comment-box').append(temp_html)
                }

            }
        });
    }

show_comment()

// 댓글 db저장
function save_comment() {
    // 입력하는 사람 정보
    //let user_name = $('#').val()
    //let post_num = $('#post_num').val()
    let comment = $('#comment').val()
    //post_num_give:post_num
    $.ajax({
        type: 'POST',
        url: '/comment',
        data: { comment_give:comment },
        success: function (response) {
            alert(response['msg'])
            window.location.reload()
        }
    });
}

