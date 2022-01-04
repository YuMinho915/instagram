// 구현정 댓글 작업==============================================================
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

// 구현정 게시물 업로드==============================================================
function posting() {
      let title = $('#title').val()
      let file = $('#file')[0].files[0]
      let form_data = new FormData()

      form_data.append("title_give", title)
      form_data.append("file_give", file)

      $.ajax({
          type: "POST",
          url: "/fileupload",
          data: form_data,
          cache: false,
          contentType: false,
          processData: false,
          success: function (response) {
              alert(response["result"])
              window.location.reload()
          }
      });
    }

    function find_img() {
      let title = $('#find_title').val()
      document.getElementById('link').href = '/fileshow/'+title
    }

    function to_post() {
        window.location.href = "/post"
    }

    function to_instagram() {
        window.location.href = "/"
    }

    function to_mypage() {
        window.location.href = "/mypage"
    }


    function q1() {
        $.ajax({
            type: "GET",
            url: "http://spartacodingclub.shop/sparta_api/rtan",
            data: {},
            success: function (response) {
                let imgurl = response['url'];
                $("#img-rtan").attr("src", imgurl);


            }
        })
    }

function turnOnOff(x) {
		if (x.src.match("like@3x")) {
			x.src = "https://cdn-icons-png.flaticon.com/512/2107/2107845.png"
		} else {
			x.src = "../static/img/like@3x.png"
		}
	}