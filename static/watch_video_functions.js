function updateLikeDislike(type) {
    const videoId = document.getElementById('videoId').innerText;
    storedLikeType = document.getElementById('storedLikeType');
    const likeCount = document.getElementById('likeCount');
    const likeButton = document.getElementById('likeButton');
    const dislikeCount = document.getElementById('dislikeCount');
    const dislikeButton = document.getElementById('dislikeButton');

    const requestOptions = {
        method: 'POST',
        headers: {
            'videoId': videoId,
            'type': type,
            'storedType': storedLikeType.innerText,
            'likeCount': likeCount.innerText,
            'dislikeCount': dislikeCount.innerText
        }
    };

    fetch("/video/likeDislike", requestOptions)
        .then((res) => res.json())
        .then((data) => {
            likeCount.innerHTML = data['likeCount'];
            dislikeCount.innerHTML = data['dislikeCount'];
            storedLikeType.innerHTML = type;
            if (type === 'like') {
                likeButton.className = "bi bi-hand-thumbs-up-fill";
                likeButton.setAttribute('onclick', "updateLikeDislike('')");
                dislikeButton.className = "bi bi-hand-thumbs-down";
                dislikeButton.setAttribute('onclick', "updateLikeDislike('dislike')");
            } else if (type === 'dislike') {
                likeButton.className = "bi bi-hand-thumbs-up";
                likeButton.setAttribute('onclick', "updateLikeDislike('like')");
                dislikeButton.className = "bi bi-hand-thumbs-down-fill";
                dislikeButton.setAttribute('onclick', "updateLikeDislike('')");
            } else {
                likeButton.className = "bi bi-hand-thumbs-up";
                likeButton.setAttribute('onclick', "updateLikeDislike('like')");
                dislikeButton.className = "bi bi-hand-thumbs-down";
                dislikeButton.setAttribute('onclick', "updateLikeDislike('dislike')");
            }
        })
}


function deleteComment(commentId) {
    const comment = document.getElementById('userComment-' + commentId);
    const delBtn = document.getElementById('delBtn-' + commentId);
    const br = document.getElementById('br-' + commentId);
    
    // hide comment from user
    comment.style.display = 'none';
    delBtn.style.display = 'none';
    br.style.display = 'none';

    // send delete request to Azure
    const requestOptions = {
        method: 'POST',
        headers: {
            'commentId': commentId,
        }
    };

    fetch("/video/comment_delete", requestOptions)
}