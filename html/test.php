<head>
    <meta charset="UTF-8">
    <title>niconicoMirror</title>
</head>

<video id="video1" width="100%" height="25%" preload="auto" controls autoplay></video>
<table>
    <tr>
        <th style="width:20%;height:10%">
            <button onclick="video_elem.requestFullscreen();" style="width:100%;height:100%;" >全画面モード</button>
        </th>
        <th style="width:1%;height:10%">
            <input type="checkbox" id="auto">
        </th>
        
        <th style="width:80%;height:10%">
            <span id="console"></span>
        </th>
    </tr>
</table>

<script type="text/javascript">
    let playing_id = 0;
    let video_elem = document.getElementById("video1");
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
            dir.split("/").forEach((element)=>{
                uri += "/" + encodeURIComponent(element);
                document.getElementById("console").innerText = element;
            });
            cookieArray = getCookieArray();
            video_elem.src = uri;
            if (typeof cookieArray[encodeURIComponent(dir)] !== 'undefined'){
                video_elem.currentTime = Number(cookieArray[encodeURIComponent(dir)]);
            }
            return true;
        }
    }
    video_elem.addEventListener('timeupdate', function() {
        let dir = document.getElementById("f_"+playing_id).innerText.replace("\n","");
        document.cookie = encodeURIComponent(dir) + "=" + video_elem.currentTime + ";max-age=" + 60*60*24*7;
        if (video_elem.duration-0.5 <= video_elem.currentTime){
            if(document.getElementById("auto").checked){
                video_elem.currentTime = 0;
                if(!change(Number(playing_id)+1)){
                    video_elem.src = null;
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
        // フォルダの寿命確認-------------------------------------
        if(!strcmp($dirname[0], "_")){
            if(!file_exists($dirname.'/create.txt')){
                file_put_contents($dirname.'/create.txt', time());
            }
            $unit_time = (int)file_get_contents($dirname.'/create.txt');				
            $alive_time = $unit_time + (1 * 24 * 60 * 60) - time(); // 1週間
            if(0 > $alive_time){
                system("rm -rf {$dirname}");
                continue;
            }
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
                        if (!($s_filename[1] == 'original.mp4' || $s_filename[1] == 'paint.mp4')){
                            echo '<button id="f_'.$counter.'" style="width:100%;height:100px;" onclick="change(\''.$counter
                            .'\');"><span style="font-size:1px;">'.$s_filename[0].'/</span><br/><span style="font-size:24px;">'.$s_filename[1].'</span></button>';
                            $counter += 1;
                        }
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

