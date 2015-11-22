// Requires: 
// <script src="three.min.js"></script>
// <script src="objstl.js"></script>
// <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>

// <div id="webgl"> is where the 3d stuff will be crammed in to

$(document).ready(function() { 
	load();
	
	// Don't ask :p
	$('body').append('<div id="centered" class="centered" ></div>');
})

function loadStl(url) {
		var xhr = new XMLHttpRequest();
		xhr.open('GET', url, true);

		xhr.responseType = 'arraybuffer';

		xhr.onload = function(e) {
				if (this.status == 200) {
					var u8 = new Uint8Array(this.response);
					var i, len = u8.byteLength, stl = "";
					for (i=0; i<len; i++) {
						stl  += String.fromCharCode(u8[i]);
					}

					f = {name: url};
                    buildGeometry(stl, f);     						
				} else {
					console.log("Got status code " + this.status + " trying to load STL file.");
				}							
		}
		xhr.onerror = function(e) {
			console.log("Error loading STL over AJAX, " + e);
		}

		xhr.send();                                       
}
