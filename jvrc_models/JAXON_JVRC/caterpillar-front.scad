module oval(clength, cradius, cthick) {
	rotate([90,0,0]) union() {
		translate([clength/2,0,0]) cylinder(h = cthick,r = cradius, center = true);
		translate([-clength/2,0,0]) cylinder(h = cthick, r = cradius, center = true);
		cube(size = [clength, cradius*2, cthick], center = true);
	}
}
module caterpillar(clength, cradius, cthick) {
	color([0.1,0.1,0.1,1]) {
		difference() {
			oval(clength, cradius, cthick);
			oval(clength, cradius*0.9, cthick*1.1);
		}
	}
	color([0.8,0.8,0.8,1]) {
		oval(clength, cradius*0.9, cthick);
	}
}

translate([30, 0, 0]) caterpillar(60, 8, 8);
