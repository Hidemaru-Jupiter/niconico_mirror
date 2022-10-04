<head>
    <meta charset="UTF-8">
    <title>niconicoMirror</title>
</head>

<script src="DPlayer.min.js"></script>
<div id="dplayer" style="width:100%;height:25%;"></div>
<script>
    const dp = new DPlayer({
        container: document.getElementById('dplayer'),
        screenshot: true,
        video: {
            thumbnails:''
        },
        danmaku:{
            id:"test",
        },
    });
</script>
<table>
    <tr>
        <th style="width:20%;height:10%">
            <button onclick="dp.video.requestFullscreen();" style="width:100%;height:100%;" >全画面モード</button>
        </th>
        <th style="width:1%;height:10%">
            <input type="checkbox" id="auto" checked>
        </th>
        
        <th style="width:80%;height:10%">
            <span id="console"></span>
        </th>
    </tr>
</table>

<script type="text/javascript">
    let playing_id = 0;
    let dialog = document.getElementById("dialog");
    
    //cookie値を連想配列として取得する
    function getCookieArray(){
        var arr = new Array();
        if(document.cookie != ''){
            var tmp = document.cookie.split('; ');
            for(var i=0; i<tmp.length; i++){
            var data = tmp[i].split('=');
            arr[data[0]] = decodeURIComponent(data[1]);
            }
        }
        return arr;
    }
    
    function change(id){
        playing_id = id;
        console.log(playing_id);
        let id_elem = document.getElementById("f_"+id)
        if(id_elem === null){
            return false;
        }else{
            let dir = id_elem.innerText.replace("\n","");
            let uri = ".";
            uri_dir = "./" + encodeURIComponent(dir.split("/")[0]) + "/";
            document.getElementById("console").innerText = dir.split("/")[1];
            cookieArray = getCookieArray();
            dp.switchVideo(
                {
                    url: uri_dir + encodeURIComponent('original.mp4'),
                    pic: uri_dir + encodeURIComponent('thumbnail.jpg'),
                    thumbnails: uri_dir + encodeURIComponent('hconcat100_thumbnail.jpg'),
                },
                {
                    id: dir.split("/")[1],
                    api: uri_dir + 'comment.txt'
                }
            );
            if (typeof cookieArray[encodeURIComponent(dir)] !== 'undefined'){
                dp.video.currentTime = Number(cookieArray[encodeURIComponent(dir)]);
            }
            dp.video.play();
            return true;
        }
    }
    dp.video.addEventListener('timeupdate', function() {
        let dir = document.getElementById("f_"+playing_id).innerText.replace("\n","");
        document.cookie = encodeURIComponent(dir) + "=" + dp.video.currentTime + ";max-age=" + 60*60*24*7;
        if (dp.video.duration-0.5 <= dp.video.currentTime){
            if(document.getElementById("auto").checked){
                if(!change(Number(playing_id)+1)){
                    dp.video.currentTime = 0;
                }
            }
        }
    });
</script>
<div style="width:100%;height:70%;overflow-y:scroll;">
<?php
//Get a list of file paths using the glob function.
$dirList = glob('*',GLOB_ONLYDIR);
echo '<table>';
    $counter = 0;
    foreach($dirList as $dirname){
        if(!strcmp($dirname[0], "_")){
            continue;
        }
        // フォルダの寿命確認-------------------------------------
            if(!file_exists($dirname.'/create.txt')){
                file_put_contents($dirname.'/create.txt', time());
            }
            $unit_time = (int)file_get_contents($dirname.'/create.txt');				
            $alive_time = $unit_time + (1 * 24 * 60 * 60) - time(); // 1日
            if(0 > $alive_time){
                system("rm -rf {$dirname}");
                continue;
            }
        // ----------------------------------------------------
        echo '<tr style="background-color:black;">';
            if (file_exists($dirname.'/thumbnail.jpg')){
                echo '<th style="width:50%;">';
                    echo '<div style="position:relative;">';
                        echo '<p style="position:absolute;color:white;font-size:24px;-webkit-text-stroke:1px #000;">'.$alive_time.'</p>';
                        echo '<img src="'.$dirname.'/thumbnail.jpg" width="auto" height="288px"/>';
                    echo '</div>';
                echo '</th>';
                // 動画ファイルのボタン化-------------------------------------
                echo '<th style="width:50%;"><div style="height:288px;overflow-y:scroll;">';
                $contentsList = glob($dirname.'/*');
                sort($contentsList, SORT_NATURAL | SORT_FLAG_CASE);
                foreach($contentsList as $filename){
                    if (preg_match('/\.(avi|flv|mkv|mov|mp4|webm)/', $filename) == 1){
                        $s_filename = explode('/', $filename);
                        echo '<button id="f_'.$counter.'" style="width:100%;height:100px;" onclick="change(\''.$counter
                        .'\');"><span style="font-size:1px;">'.$s_filename[0].'/</span><br/><span style="font-size:24px;">'.$s_filename[1].'</span></button>';
                        $counter += 1;
                    }
                }
                echo '</div></th>';
                // -------------------------------------------------------
            }
        echo '</tr>';
    }
echo '</table>';
?>
</div>

