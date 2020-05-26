/**
 * @author richt / http://richt.me
 * @author WestLangley / http://github.com/WestLangley
 *
 * W3C Device Orientation control (http://w3c.github.io/deviceorientation/spec-source-orientation.html)
 */

THREE.DeviceOrientationControls = function( object ) {

	var scope = this;

	this.object = object;
	this.object.rotation.reorder( "YXZ" );

	this.enabled = true;

    this.deviceOrientation = {};
    this.initialOrientation = {};
    this.afterfirst = false;
	this.screenOrientation = 0;

	this.alphaOffset = 0; // radians

	var onDeviceOrientationChangeEvent = function( event ) {

		scope.deviceOrientation = event;
        if ((scope.afterfirst) == false) {
        //
            scope.initialOrientation = event;
            scope.afterfirst = true;
        }
	};

	var onScreenOrientationChangeEvent = function() {

		scope.screenOrientation = window.orientation || 0;

	};

	// The angles alpha, beta and gamma form a set of intrinsic Tait-Bryan angles of type Z-X'-Y''

	var setObjectQuaternion = function() {

		var zee = new THREE.Vector3( 0, 0, 1 );

		var euler = new THREE.Euler();

		var q0 = new THREE.Quaternion();

		//var q1 = new THREE.Quaternion( - Math.sqrt( 0.5 ), 0, 0, Math.sqrt( 0.5 ) ); // - PI/2 around the x-axis

		return function( quaternion, alpha, beta, gamma, orient ) {

			euler.set( beta, alpha, - gamma, 'YXZ' ); // 'ZXY' for the device, but 'YXZ' for us

			quaternion.setFromEuler( euler ); // orient the device

			//quaternion.multiply( q1 ); // camera looks out the back of the device, not the top

			quaternion.multiply( q0.setFromAxisAngle( zee, - orient ) ); // adjust for screen orientation

		}

	}();

	this.connect = function() {

		onScreenOrientationChangeEvent(); // run once on load

		window.addEventListener( 'orientationchange', onScreenOrientationChangeEvent, false );
		window.addEventListener( 'deviceorientation', onDeviceOrientationChangeEvent, false );

		scope.enabled = true;

	};

	this.disconnect = function() {

		window.removeEventListener( 'orientationchange', onScreenOrientationChangeEvent, false );
		window.removeEventListener( 'deviceorientation', onDeviceOrientationChangeEvent, false );

		scope.enabled = false;

	};

	this.update = function() {

		if ( scope.enabled === false ) return;

        var device = scope.deviceOrientation;
       
        var initial = scope.initialOrientation;
        

        if (device) {     

            var alpha = device.alpha ? THREE.Math.degToRad(device.alpha - initial.alpha  ) : 0; // Z
        
            var beta = device.beta ? THREE.Math.degToRad(device.beta -initial.beta ) : 0; // X'

            var gamma = device.gamma ? THREE.Math.degToRad(device.gamma - initial.gamma ) : 0; // Y''
            
			var orient = scope.screenOrientation ? THREE.Math.degToRad( scope.screenOrientation ) : 0; // O
            
            if (alpha == 0 && beta == 0 && gamma==0 && orient==0) {
               
                //orient = ;
            }
			//setObjectQuaternion( scope.object.quaternion, 0, 0, 0, 0 );
            setObjectQuaternion(scope.object.quaternion, beta, gamma, alpha, orient);
            //setObjectQuaternion(scope.object.quaternion, alpha, beta, gamma, orient);
		}


	};

	this.dispose = function() {

		scope.disconnect();

	};

	this.connect();

};