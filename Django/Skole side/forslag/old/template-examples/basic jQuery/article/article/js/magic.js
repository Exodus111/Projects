/**
	function used to expand any object to an array for debug help. Knd of the same as a toString in java.
*/
function toString(myArray) {
	var toReturn = '';
	var x;
	for(x in myArray) {
		if(myArray[x]==null) {toReturn += x+':null, '} 
		else if (typeof myArray[x]=="object") {
			toReturn += x+':['+toString(myArray[x])+'], ';
		} else {
			toReturn += x+':'+myArray[x]+', ';}
		}
	return toReturn;
};
/**
	the design jquery plugin
*/
jQuery.design= {
	/** used to lock critical functions */
	locked : {align:false, unAlign:false, limit:false, createGhost:false}, 			//lock manip on current elements
	/** Array containing all the options and alignfunctions of all aligned elements. Key value are the ids of the elements */
	alignTargets : [],		//all the elements (id) which are aligned
	/** Array containing for each element all the ids of the element that are aligned to him */
	alignWatchers : [],		//all the elements (id)which are aligned to
	/** Array containing for each element its limit options, its activated limits and a private used startLimitValue */
	limit : [],				
	/** Array containing for each menu (ul element) its subMenu li and for each subMenu li its option and subMenu element */
	menu : [],				
	/** Array containing for each element its associated ghost'id */
	ghosts : [],			
	/** Array containing timers of specific elements (id) */
	timers : [],
	/** fast acces browser information */			
	browser : {
		ie6 : (($.browser.msie && $.browser.version=="6.0")) ? true : false, //detect ie6
		iStuff : (navigator.platform == 'iPad' || navigator.platform == 'iPhone' || navigator.platform == 'iPod') ? true:false,
		iPad : navigator.platform == 'iPad', 
		/** is the browser accepting fixed property in css */
		fixedSupport : !(($.browser.msie && $.browser.version=="6.0")|| (navigator.platform == 'iPad' || navigator.platform == 'iPhone' || navigator.platform == 'iPod'))
	}, 
	/** default accion of the menu depends if it is smartphone or mouse */
	defaultAction : (navigator.userAgent.match(/Android/i) || navigator.userAgent.match(/webOS/i) || navigator.userAgent.match(/iPhone/i) ||navigator.userAgent.match(/iPod/i)) ? "click": "over",
	/** may be usefull */
	staticClass:"fixed",
	/** in case we bind body */
	bodyWrapper : $(window),
	/** in case we bind body */
	bodyContainer : $(window), 
	/** usefull list functions */
	tools : {
		areHashEqual : function (array1, array2) {
			for (var i in array1) {
				if(array2[i] == undefined || array1[i] != array2[i]){return false;}
			}
			return true;
		}, 
		/**
		 * remove duplicates elements in an array
		 */
		removeDuplicates : function (a) {
		   var r = [];
		   o:for(var i = 0, n = a.length; i < n; i++) {
		      for(var x = 0, y = r.length; x < y; x++){ 
		      	if(r[x]==a[i]) {continue o;}
		      	if(typeof r[x] == "object" && typeof a[i] == "object" && $.design.tools.areHashEqual(r[x], a[i])) {continue o;};
		      }
		      r[r.length] = a[i];
		   }
		   return r;
		},
		/**
		 * remove an element in an array
		 */
		removeItems : function (originalArray, itemsToRemove) {
			if(!originalArray || !itemsToRemove) {return originalArray;}
			var j;
			for (var i = 0; i < itemsToRemove.length; i++) {
				j = 0;
				while (j < originalArray.length) {
					if (originalArray[j] == itemsToRemove[i] || (typeof originalArray[j] =="object" && typeof itemsToRemove[i] == "object" &&  $.design.tools.areHashEqual(originalArray[j], itemsToRemove[i]))) { originalArray.splice(j, 1);} 
					else {j++;}
				}
			}
			return originalArray;
		}
	}, 
	/** tool to have quick acces to direction proccess  */
	coord : {
		/************** private data **************/
		dir : {
		top:-1,			topIsBottomOf:-3,			/* VERTICAL   % 2  != 0 */
		right:2, 		rightIsLeftOf:4,			/* HORIZONTAL % 2  =  0 */
		bottom:1, 		bottomIsTopOf:3,			/* direction = - opositeDirection */
		left:-2, 		leftIsRightOf:-4,			/* infDirection < 0	  &  supDirecton > 0 (ex : top < 0 & bottom>0)	*/ 
		center:0
		},
		/** Array used to cache the coordinates values */
		useCache : true , cache : [], clearCache : function(x) {$.design.coord.cache = []},
		/************** coordinates functions **************/
		/** return if true/false the given parameter is a direction */
		isDirection : function(x) {return (this.dir[x]!=undefined);},
		/** return if true/false the directionis vertical */
		isVertical : function(x) {return (this.dir[x]==0 || (this.dir[x] % 2 != 0));},
		/** return if true/false the directionis horizontal */
		isHorizontal : function(x) {return (this.dir[x] % 2 == 0);},
		/** return if true/false the direction given is max value (ex bottom => true, top => false) */
		isMaxValue : function (x) {if (this.dir[x]>0) {return true;} else {return false;}},
		/** target : topIsBottomOf -> bottom */
		target : function(x) {if(Math.abs(this.dir[x])>2) {return $.design.coord.side($.design.coord.opposite(x));} return x;},
		/** return the distance to the opposite direction for the given element */
		distanceToOpposite : function (element, x) {
			if(this.isVertical(x)){if(this.dir[x]<0) {return element.height();} else {if(this.dir[x]==0){return 0;} else {return - element.height();}}}
			else {if(this.dir[x]<0) {return element.width();} else {return - element.width();}}
		},
		/** return the opposite direction */
		opposite : function (x) {for(var y in this.dir) { if (this.dir[x] == - this.dir[y]) {return y;}}return null;},
		/** return the side of the direction, if "center" return center */
		side : function (x) {
			if(this.isVertical(x)){if(this.dir[x]<0) {return "top";} else {if(this.dir[x]==0){return "center";} else {return "bottom";}} }
			else {if(this.dir[x]<0) {return "left";} else {return "right";}}
		}
	}, 
	applyPosition : function (target, targetId, options) {delete $.design.coord.cache[targetId];target.css(options);}, 
	/** init function for the plugin */
	init : function() {
		/** function to apply css orders (the options will contains 'center' property to explode into correct left/right */
		if ($.design.coord.useCache) {
			$.design.bodyWrapper.bind('scroll', $.design.coord.clearCache);
			$.design.bodyWrapper.bind('resize',  $.design.coord.clearCache);
		}
		if(!($.design.browser.fixedSupport)) {
			var alignFunction = function() {
				$.design.coord.clearCache();
				for(x in $.design.alignTargets) {
					var me = $("#"+x);
					if(me==null) {continue;}
					if($.design.alignTargets[x]) {
						$.design.alignTargets[x].alignFunction();
						me.refreshAlignWatchers();	
					}

				}
				for(x in $.design.limit) {
					var me = $("#"+x);
					if(me==null) {continue;}
					me._limit();
				}
				return false;
			};
			if($.design.browser.iStuff) {window.onscroll = alignFunction;} 
			else {$.design.bodyWrapper.bind('scroll', alignFunction);}
			$.design.bodyWrapper.bind('resize', alignFunction);
			$('.fixed').each(function(){
					var target = $(this);
					target = target.setPosition('fixed');	//set good position stuff						
			});		
		}
	}
};
(function($) {
		$.fn.virtualScroll = function() {
			var result = {left: $(window).scrollLeft(), top:$(window).scrollTop()};
			return result; 
		};
		/**
		    get the id of the element, if id is null, we set a random Id
		    @name getNotNullId
		    @function
		    @return a string which is the id of the element
		*/	
        $.fn.getNotNullId = function(){
			if($(this).parent().length>0) {
				var toReturn = $(this).attr('id'); if(!toReturn){toReturn = "me-" + Math.floor(Math.random()*10000); $(this).attr('id', toReturn);}
				return toReturn;
			} else {return "";} //this is the window
		};
		/**
		    
		*/	
		
		$.fn.refreshAlignWatchers = function(myId){
			if(myId==undefined) {myId = $(this).getNotNullId();}
			if($.design.alignWatchers[myId] != undefined) {
				$.each($.design.alignWatchers[myId], function(index, value) { 	
					//if($.design.limit[value]) {$("#"+value)._executeLimit();}
					$("#"+value).align($.design.alignTargets[value].options);
				});
    		}
			var childTargets= $(this).find('.alignTarget');
			$.each(childTargets, function() { 
				childTargetId = $(this).getNotNullId();	
				if($.design.alignWatchers[childTargetId] != undefined) {
					$.each($.design.alignWatchers[childTargetId], function(index, value) { 
						if($.design.alignTargets[value]) {$("#"+value).align($.design.alignTargets[value].options);}
					});
				}
			}); 
		};
		/**
		    get the coordinate of a single jquery object
		    @function
		    @return an array containing the asked coordinates
		*/	
		$.fn.coordinates = function(options)
        {
        	var returnSingleValue = null; var returnAll=false;
        	if(options==undefined || options==null){returnAll = true;}
        	else if (typeof options == "string") {returnSingleValue = options;options = [];options[returnSingleValue]=true; } 
			var toReturn = [];
			var myId = $(this).getNotNullId();
			if($.design.coord.useCache && $.design.coord.cache[myId]) {
				if(returnAll) {return $.design.coord.cache[myId];}
				for (var x in options) {if(options[x]==true) toReturn[x] = $.design.coord.cache[myId][x];}
			} else {
				$.design.coord.cache[myId] = [];
				var offset= $(this).offset();if(!offset) {offset = $(this).virtualScroll();}
	    		if(!offset){offset = $(window).virtualScroll();}
				$.design.coord.cache[myId] = {
					width:$(this).width(), height:$(this).height(), 
					top : offset.top, left : offset.left
				};
				$.design.coord.cache[myId].right = offset.left+$.design.coord.cache[myId].width; 
				$.design.coord.cache[myId].bottom = offset.top+$.design.coord.cache[myId].height;
				if(returnAll) {return $.design.coord.cache[myId];}
				for (var x in options) {if (options[x] == true) toReturn[x] = $.design.coord.cache[myId][x];}
			}
        	if(returnSingleValue) {return toReturn[returnSingleValue];}
			return toReturn;
        };
		/**
		 * given absolutes coordinates, return these coordinates in the frame of reference of this
		 * @param {Object} options
		 */
		$.fn.coordinatesOf = function(options)
        {
        	var me = $(this);
        	var returnSingleValue = null;
        	if (typeof options == "string") {returnSingleValue = options; } 
        	var myCoordinates = me.coordinates();
        	var toReturn = [];
        	for(var x in options) {
        		if(!$.design.coord.isDirection(x) || options[x]=="auto") {toReturn[x]=options[x];continue;}
        		var myCoord = (myCoordinates[x] != undefined ? myCoordinates[x] : 0); //if x=="center" just keep the coordinate intact 
        		if($.design.coord.isMaxValue(x)) {toReturn[x] = myCoord - options[x];} 
				else {toReturn[x] = options[x] - myCoord;}
        	}
        	if(returnSingleValue){return toReturn[returnSingleValue];}
        	return toReturn;
        };
	
		/**
		    set the limit of the element same parameters than align
		    @name limit
		    @function
		*/	
		$.fn.limit = function(options)
        {
			if (typeof options == "string") {
				var defaults = {top: options,  right: options,  bottom: options,  left: options	};  
			} 
			else {var defaults = {	}; }
			var options = $.extend(defaults, options);  
			return this.each(function() { 
				var target = $(this);
				var targetId = target.getNotNullId();
				//stock the last limit desired
				var optionsToSet = [];
				for(var option in options) {
					var side = $.design.coord.side(option);
					optionsToSet[side] = {direction:option, id:options[option]};
				}
				$.design.limit[targetId] = {options: optionsToSet, unAligned: [], startLimitValue: []};
				if($.design.browser.fixedSupport) {
					$.design.bodyWrapper.bind("scroll", function() {$('#'+targetId)._limit();});
					$.design.bodyWrapper.bind("resize", function() {$('#'+targetId)._limit();});
				}		
			}); 
        };
		/**
		 * for previous compatibility
		 */
		$.fn.setLimit = function(options) {this.limit(options);};
		
		/**
		 * private
         * limit is called for each scroll/resize for elements who have limits activated
		 */ 
        $.fn._limit = function(){if ($.design.locked.limit == false) {this._executeLimit();}};
    	
    	/**
    	 * private
    	 * the critical section function limit
    	 */
		$.fn._executeLimit = function()
        {
        		//in case we are locked, cancel
				if ($.design.locked.align == true || $.design.locked.unAlign == true || $.design.locked.createGhost == true) {return;}
				var target = $(this); var targetId = target.attr('id');
				var originalTarget = $(this); var originalTargetId = targetId;
				$.design.locked.limit=true;
				//process stuffs on temp vars to reduce risks if we are called an other time
	    		var tempLimitOriginalTargetId = $.design.limit[originalTargetId];
				if(!tempLimitOriginalTargetId){return;}	
				
				// if has ghost apply on ghost 
				if($.design.ghosts[targetId] != null && ($.design.ghosts[targetId] != undefined)) {
	    			targetId = $.design.ghosts[targetId];
	    			target = $('#'+targetId);
	    		}
				
				//process the area used by the target / the area the target would have if not limited  
				var area = {left:null, top:null, right:null, bottom:null};
				var targetCoordinates = target.coordinates();
				area.height = targetCoordinates.height; area.width = targetCoordinates.width;
				if ($.design.alignTargets[originalTargetId]) {
					for (var u in $.design.alignTargets[originalTargetId].options) {
						if($.design.alignTargets[originalTargetId].options[u] == null || !$.design.coord.isDirection(u)){continue;}
						var alignedId = $.design.alignTargets[originalTargetId].options[u];
						var side = $.design.coord.side(u);
						var targetDirection = $.design.coord.target(u);
						var oppositeSide = $.design.coord.opposite(side);
						if(alignedId=='') {var aligned = $(window);} 
						else {var aligned = $("#"+($.design.ghosts[alignedId] != null ? $.design.ghosts[alignedId] : alignedId));}
						var myOffset = $.design.alignTargets[originalTargetId].options.offset[side] ? $.design.alignTargets[originalTargetId].options.offset[side] :0;
						var offsetToAdd = $.design.coord.isMaxValue(targetDirection) ? -myOffset : myOffset;
						area[side] = {
							value : aligned.coordinates(targetDirection)+offsetToAdd,
							direction : u,
							id : alignedId, 
							offset:myOffset
						};
						if(!area[oppositeSide]) {
							area[oppositeSide] = {
								value:area[side].value + $.design.coord.distanceToOpposite(target, side), 
								direction:u, 
								id:alignedId,
								offset : myOffset
							};
						}
					}
				}
				
				var unAlignedArea = {left:null, top:null, right:null, bottom:null};
				for (var side in tempLimitOriginalTargetId.unAligned) {
					var oppositeSide = $.design.coord.opposite(side);
					var isMaxSide = $.design.coord.isMaxValue(side);
					var distanceToOppositeSide = $.design.coord.distanceToOpposite(target, oppositeSide);
					if(!tempLimitOriginalTargetId.unAligned[side]) {continue;}
					for (var index = 0; index < tempLimitOriginalTargetId.unAligned[side].length; index++) {
						var unAligned = tempLimitOriginalTargetId.unAligned[side][index];
						//get the jquery element of this unAligned
						if(unAligned.id=='') {var unAlignedElement = $(window);} 
						else {var unAlignedElement = $("#"+($.design.ghosts[unAligned.id] != null ? $.design.ghosts[unAligned.id] : unAligned.id));}
						var offsetToAdd = $.design.coord.isMaxValue(unAligned.direction) ? -unAligned.offset : unAligned.offset;
						
						//get the target direction
						var unAlignedDirectionTarget = $.design.coord.target(unAligned.direction);
						
						//get the values of this unaligned
						var tempAreaSide = {
							direction : unAligned.direction,
							id : unAligned.id,
							value : unAlignedElement.coordinates(unAlignedDirectionTarget)+offsetToAdd, 
							offset : unAligned.offset
						};
						
						if(oppositeSide == $.design.coord.side(unAligned.direction)) {tempAreaSide.value += distanceToOppositeSide;} //we may have to add the width or height of target
						
						var tempAreaOppositeSide = {
							value:tempAreaSide.value+ $.design.coord.distanceToOpposite(target, side), 
							direction : tempAreaSide.direction, 
							id : tempAreaSide.id, 
							offset : unAligned.offset
						};
						var outsideSide = unAlignedArea[side] 
							&& ((((tempAreaSide.value < unAlignedArea[side].value) == isMaxSide)|| (tempAreaSide.value == unAlignedArea[side].value))	/* is better or same align */
							&& (
								(($.design.coord.side(tempAreaSide.direction)==side) && tempAreaSide.value == unAlignedArea[side].value) 				/* AND     is direct align and not indirect, apply even if equal to previous value */
								|| (tempAreaSide.value != unAlignedArea[side].value)																			/* OR is better align */
							));
						var outsideOppositeSide = unAlignedArea[oppositeSide] 
							&& ((((tempAreaOppositeSide.value < unAlignedArea[oppositeSide].value) == isMaxSide) || (tempAreaOppositeSide.value == unAlignedArea[oppositeSide].value))
							&& (
								(($.design.coord.side(tempAreaSide.direction)==oppositeSide) && tempAreaSide.value == unAlignedArea[side].value) 
								|| (tempAreaOppositeSide.value != unAlignedArea[oppositeSide].value))
							);
						if(!unAlignedArea[side] || outsideSide) {
							unAlignedArea[side] = tempAreaSide;
							unAlignedArea[side].unAligned = unAligned;
						}
						if(!unAlignedArea[oppositeSide]  || outsideOppositeSide) {
							unAlignedArea[oppositeSide] = tempAreaOppositeSide;	
							unAlignedArea[oppositeSide].unAligned = unAligned; 
						}	
					}
						
				}
				for (var x in area)	{ if(!area[x]) {area[x] = {value:targetCoordinates[x], direction:x, id:originalTargetId, offset:0};}}
				
				var unAlignParams = {}; var alignParams = {};
				var limitsActivated = {};var limitsUnactivated = {};
				var alignNeeded = false;var unAlignNeeded = false;
				var throwNewActiveLimitsEvent =false;var throwNewUnactiveLimitsEvent =false;
				var clip={};
				for (var x in tempLimitOriginalTargetId.options) { 
					//process the limit's clip of the target for each direction x
					if (tempLimitOriginalTargetId.options[x].id == null || tempLimitOriginalTargetId.options[x].id == undefined) {continue;}
					var element = null;var elementId = null; var originalElementId = null;
					if (tempLimitOriginalTargetId.options[x].id == '') {element = $(window);elementId = '';originalElementId=''}
					else {
						originalElementId = tempLimitOriginalTargetId.options[x].id;
						elementId = $.design.ghosts[tempLimitOriginalTargetId.options[x].id] != null ? $.design.ghosts[tempLimitOriginalTargetId.options[x].id] : tempLimitOriginalTargetId.options[x].id;
						element = $("#" + elementId);
					}
					if(elementId != "" && !element.is(":visible")) {continue;} /* if the element is not visible the offset() will return (0, 0), let's skip this element until it's visible */
					
					var side = $.design.coord.side(x);
					var isMaxSide = $.design.coord.isMaxValue(side);
					var oppositeSide = $.design.coord.opposite(side);
					var distanceToOpposite = $.design.coord.distanceToOpposite(target, side);
					
					var tempValue = element.coordinates($.design.coord.target(tempLimitOriginalTargetId.options[x].direction));
					var tempOppositeValue = tempValue + distanceToOpposite;
					
					var outsideSide = (clip[side] && ((tempValue < clip[side].value) == isMaxSide) && (tempValue != clip[side].value));
					var outsideOppositeSide = (clip[oppositeSide] && ((tempOppositeValue < clip[oppositeSide].value) == isMaxSide) && (tempOppositeValue != clip[oppositeSide].value));
						
					if(!clip[side] || (outsideOppositeSide && outsideSide)) {
						clip[side]={
							offset : 0,
							value:tempValue, 
							direction:tempLimitOriginalTargetId.options[x].direction, 
							id:originalElementId, 
							active : area[side].id == originalElementId && tempLimitOriginalTargetId.options[x].direction == area[side].direction 				
						};
						
						if(clip[side].active && clip[oppositeSide]  && !clip[oppositeSide].active) {
							delete clip[oppositeSide];
						}
					}
				}
				for(var side in clip) {	
					var isMaxSide = $.design.coord.isMaxValue(side);
					var oppositeSide = $.design.coord.opposite(side);
					
					if(clip[side].active) {
						//check if we have to unLimit
						var currentLimitValue =  tempLimitOriginalTargetId.startLimitValue[side];
						if (((area[side].value < clip[side].value) == isMaxSide && area[side].value != clip[side].value) || 		//current align is no more outside the clip
							((area[side].value > currentLimitValue) == isMaxSide && area[side].value != currentLimitValue) ||		//OR get beyond the limit launch
							((unAlignedArea[side]!=null || unAlignedArea[side]!=undefined) && ((unAlignedArea[side].value < clip[side].value) == isMaxSide))			//OR previous aligned exists and is inside the clip area
						) {	// UN-LIMIT
							delete tempLimitOriginalTargetId.startLimitValue[side];
							if (!unAlignParams[side]) {
								unAlignNeeded=true;
								unAlignParams[side] = clip[side];
								throwNewUnactiveLimitsEvent = true;
								limitsUnactivated[clip[side].direction] = clip[side].id;
							}
							if(unAlignedArea[side] && unAlignedArea[side].unAligned) {
								alignNeeded = true;
								alignParams[side] = unAlignedArea[side].unAligned
							}
							if(unAlignedArea[oppositeSide] && unAlignedArea[oppositeSide].unAligned ) {
								alignNeeded = true;
								alignParams[oppositeSide] = unAlignedArea[oppositeSide].unAligned
							}
						}
					} else {
						//check if we have to limit
						if (((area[side].value > clip[side].value) == isMaxSide)) {	
							// LIMIT
							tempLimitOriginalTargetId.startLimitValue[side] = area[side].value;
							//we'll have to align stuffs
							alignNeeded=true; throwNewActiveLimitsEvent = true;
							
							//overwrite alignParam
							alignParams[side] = clip[side];
							
							throwNewActiveLimitsEvent = true;
							limitsActivated[clip[side].direction] = clip[side].id;
							
							//don't overwrite unAlignParam
							if (!unAlignParams[side] && area[side].id != originalTargetId) {
								unAlignNeeded = true; unAlignParams[side] = area[side];
							}	
							if (!unAlignParams[oppositeSide] && area[oppositeSide].id != originalTargetId && area[side].id == area[oppositeSide].id && area[side].direction == area[oppositeSide].direction) {
								//if we are only aligned to one element in side + opposite side, we unaligned it also in the opposite side
								unAlignNeeded = true; unAlignParams[oppositeSide] =  area[oppositeSide];
							}
						}
					}
				}
				//add new unaligned params to unaligned hash table
				for (var i in unAlignParams) {
					if(!tempLimitOriginalTargetId.unAligned[i]) {tempLimitOriginalTargetId.unAligned[i] = [];}
					tempLimitOriginalTargetId.unAligned[i].push({id :unAlignParams[i].id, direction : unAlignParams[i].direction, offset: unAlignParams[i].offset});
					tempLimitOriginalTargetId.unAligned[i] = $.design.tools.removeDuplicates(tempLimitOriginalTargetId.unAligned[i]);
				}
				delete tempLimitOriginalTargetId;
				if(unAlignNeeded) {
					var unAlignParamsValues = [];
					for (var k in unAlignParams) unAlignParamsValues[unAlignParams[k].direction] = unAlignParams[k].id;
					originalTarget = originalTarget.unAlign(unAlignParamsValues);
				}
				if(alignNeeded) {
					if(!$.design.ghosts[originalTargetId]) {
						originalTarget = originalTarget.createGhost(true);
						originalTarget = $("#"+originalTargetId);
					}
					//aligne mais pas marque comme limit actie
					var alignParamsValues = {offset:$.design.alignTargets[originalTargetId] ? $.design.alignTargets[originalTargetId].options.offset : []};
					for (var side in alignParams) {
						var oppositeSide = $.design.coord.opposite(side);
						if(alignParams[side].id != originalTargetId && $.design.coord.isDirection(side)) {
						 	// delete it from limit.unAligned
							alignParamsValues[alignParams[side].direction] = alignParams[side].id;
							tempLimitOriginalTargetId.unAligned[side] = $.design.tools.removeItems(tempLimitOriginalTargetId.unAligned[side], [{id:alignParams[side].id, direction:alignParams[side].direction, offset:alignParams[side].offset}]);
							tempLimitOriginalTargetId.unAligned[oppositeSide] = $.design.tools.removeItems(tempLimitOriginalTargetId.unAligned[oppositeSide], [{id:alignParams[side].id, direction:alignParams[side].direction}]);
						}
					}
					originalTarget.align(alignParamsValues);	
				}
				$.design.locked.limit = false;
				if(throwNewUnactiveLimitsEvent) {$(window).trigger("unLimit", originalTargetId, [limitsUnactivated]);}
				if(throwNewActiveLimitsEvent) {$(window).trigger("limit", originalTargetId, [limitsUnactivated]);}
				if (alignNeeded || unAlignNeeded) {
					target.refreshAlignWatchers(originalTargetId);
				}
			return;
        };

		/**
		 * aligne le composant en absolute avec les elements specifies par leur id
		 * $("#target").align({top:'elementN', right:"elementE", bottom:"elementS", left:"elementW"});
		 * possible aussi d'utiliser les paramentres : topIsBottomOf, bottomIsTopOf, rightIsLeftOf et leftIsRightOf
		 * 
		 * evidement il est possible de ne pas specifier certaines valeurs dans le cas ou on ne souhaite pas l aligner dans cette/ces direction(s)
		 * dans le cas d'un alignement total on peut faire : 
		 * $("#target").align("element");
		 * qui equivant a $("#target").align({top:'element', right:"element", bottom:"element", left:"element"});
		 */ 
        $.fn.align = function(options) {
			
			while ($.design.locked.align == true){console.log("fucked in align");} return this._executeAlign(options);			
		};
    	$.fn._executeAlign = function(options)
        {
        	if (typeof options == "string") {var options = {top: options,  right: options,  bottom: options,  left: options, offset:[]};  } 
			var defaults = {top: null, right: null, bottom: null, left: null, topIsBottomOf: null, rightIsLeftOf: null, bottomIsTopOf: null, leftIsRightOf: null, offset:[]}; 
			options =  $.extend({}, defaults, options); 
			//return this.each(function() { 
        		//init
	    		var target = $(this);
				var originalTarget = $(this);			
				var targetId = target.attr("id");
				var originalTargetId = targetId;
				var originalTargetOffset = target.coordinates();
	    		
				//manipulate temp var
	    		var tempAlignTargetsOriginalTargetId = $.design.alignTargets[originalTargetId];
				var tempAlignWatchers = $.design.alignWatchers;
				$.design.locked.align=true;
	    		if(tempAlignTargetsOriginalTargetId && tempAlignTargetsOriginalTargetId.options) {
					tempAlignTargetsOriginalTargetId.options.offset = options.offset;
					for (x in tempAlignTargetsOriginalTargetId.options) {
						if(options[x]!=null) { tempAlignTargetsOriginalTargetId.options[x]=options[x];}
					}
					options = tempAlignTargetsOriginalTargetId.options;
				}
				var fixed=false;
	    		if($.design.ghosts[targetId] != null && ($.design.ghosts[targetId] != undefined)) { //check if target has ghost if it has, we manipulate the ghost
	    			targetId = $.design.ghosts[targetId];
	    			target = $('#'+targetId);
	    		} else if(target.hasClass($.design.staticClass)){target.removeClass($.design.staticClass);}
				var papa = target.parent();
	    		//get positions
				var elements = {};
	    		var elementCounts = 0;
	    		var lastAlignedToScreen = null;
	    		var alignValues = {top:"auto",right:"auto",bottom:"auto", left:'auto'};
				for (x in options) {
					if(options[x] == null || options[x]==originalTargetId || !$.design.coord.isDirection(x)) {continue;} //do nothing if aligned to himself or to nothing

					elementCounts++;
					var elementId = $.design.ghosts[options[x]] != null ? $.design.ghosts[options[x]] : options[x];
					
					if(tempAlignWatchers[options[x]]==null) {
						tempAlignWatchers[options[x]] = new Array(originalTargetId);
					} else {
						tempAlignWatchers[options[x]].push(originalTargetId);
						tempAlignWatchers[options[x]]=$.design.tools.removeDuplicates(tempAlignWatchers[options[x]]);
					} 
					if (elementId == "") {
						elements[x] = $(window);
						if($.design.coord.isVertical(x)) {fixed=true;} //target get fixed if align to a vertical position of the screen
					}
					else {
						elements[x] = $("#" + elementId);
						if(!elements[x].hasClass("alignTarget")) {elements[x].addClass("alignTarget");}
					}
					if(elementId != "" && !elements[x].is(":visible")) {continue;} /* if the element is not visible the offset() will return (0, 0), let's skip this element until it's visible */
					if(fixed==false && (elements[x].closest('.'+$.design.staticClass).length>0)) {fixed=true;}
					var realAlignElement = null;
					var side = $.design.coord.side(x);
					alignValues[side] = elements[x].coordinates($.design.coord.target(x));
					var offsetToAdd = options.offset[side] ? ($.design.coord.isMaxValue(side) ? -options.offset[side] : options.offset[side]) : 0;
					alignValues[side] += offsetToAdd;
					//if (options.offset[side]) {alignValues[side] += options.offset[side];}
				}
				if(alignValues.left == 'auto' && alignValues.right == 'auto') {alignValues.left = originalTargetOffset.left;if(options.offset.left){alignValues.left +=options.offset.left;}}
				if(alignValues.top == 'auto' && alignValues.bottom == 'auto') {alignValues.top = originalTargetOffset.top;if(options.offset.top){alignValues.top +=options.offset.top;}}
				if(elementCounts==0){
					$.design.locked.align=false; 
					if ($.design.ghosts[originalTargetId]) {$('#'+originalTargetId).createGhost(false);}
					return;
				}
				var frameOfReference = papa;
				if(fixed && $.design.browser.fixedSupport) {
					frameOfReference = $(window);
					alignValues = $(window).coordinatesOf(alignValues);
					if (!target.hasClass($.design.staticClass)) {target.addClass($.design.staticClass);}
					if (target.hasClass("absolute")) {papa.removeClass("absolute");}
				} else {
					if (!target.hasClass("absolute")) {target.addClass("absolute");}
					if (target.hasClass($.design.staticClass)) {target.removeClass($.design.staticClass);}
					papa.css({position:'relative'});
					alignValues = papa.coordinatesOf(alignValues);
				}
				
				if(alignValues.top != "auto" && alignValues.bottom !='auto') {alignValues.height = frameOfReference.height() - alignValues.bottom - alignValues.top;}
	    		if(alignValues.right != "auto"&& alignValues.left!= "auto") {alignValues.width = frameOfReference.width() - alignValues.right - alignValues.left;}
				delete frameOfReference;
				$.design.applyPosition(target, targetId, alignValues);
				if(tempAlignTargetsOriginalTargetId==null ) {
					//if first call => bind any change
	    			tempAlignTargetsOriginalTargetId = {
	    				options : options, 
	    				alignFunction : function() {
							if($.design.alignTargets[originalTargetId]){
	    						var originalTarget = $("#"+originalTargetId);
								originalTarget.align($.design.alignTargets[originalTargetId].options);
	    					}
	    				}
	    			};
	    			originalTarget.parent().resize(tempAlignTargetsOriginalTargetId.alignFunction);
	    			if($.design.browser.fixedSupport) {$.design.bodyWrapper.resize(tempAlignTargetsOriginalTargetId.alignFunction);}
	    			
				}
	    		$.design.locked.align=false;	
				//transfer temp var to real ones
				$.design.alignWatchers = tempAlignWatchers; delete tempAlignWatchers;
				$.design.alignTargets[originalTargetId] = tempAlignTargetsOriginalTargetId ; delete tempAlignTargetsOriginalTargetId;
				
				//refresh
				var newTargetOffset = originalTarget.coordinates();
				if (!$.design.tools.areHashEqual(newTargetOffset, originalTargetOffset)) {
					target.refreshAlignWatchers(originalTargetId);
				}
			//}); 
        };
        /**
         * 	unalign the element with the options (same as align)
		 */ 
        $.fn.unAlign = function(options) {while ($.design.locked.unAlign == true){console.log("fucked in unAlign");} return this._executeUnAlign(options);};
    	$.fn._executeUnAlign = function(options){
		 	$.design.locked.unAlign=true;	
		 	var toReturn = null;
		 	if (typeof options == "string") {options = {top: options, topIsSouthOf:options, right: options, rightIsLeftOf:options, bottom: options, bottomIsTopOf:options, left: options, leftIsRightOf:options};}
		 	this.each(function(){
				var target = $(this);
				toReturn = target;
				var targetId = $(this).attr('id');
				
				//manipulate temp var
				var tempAlignTargetsTargetId = $.design.alignTargets[targetId];
				var tempAlignWatchers = $.design.alignWatchers;	
				var elementCounts=0;
				var stayingProperties=0;
				if(tempAlignTargetsTargetId!=null) {
					for(var x in tempAlignTargetsTargetId.options) {
						if(tempAlignTargetsTargetId.options[x] != null && $.design.coord.isDirection(x)){
							elementCounts++;
							if(options[x]==tempAlignTargetsTargetId.options[x]){
								tempAlignTargetsTargetId.options[x]=null;	
								$.design.tools.removeItems($.design.alignWatchers[options[x]], [targetId]); 
							} else {stayingProperties++;}
						}
					}
				}
				if(elementCounts==0){$.design.locked.unAlign=false; return;}
				if(stayingProperties==0) {
					
					if($.design.browser.fixedSupport){
						target.parent().unbind('resize', tempAlignTargetsTargetId.alignFunction);
						$.design.bodyWrapper.unbind('resize', tempAlignTargetsTargetId.alignFunction);
					}
					if($.design.locked.createGhost!=true){
						//store position in case
						target = target.createGhost(false);
						toReturn = target;
					}
					tempAlignTargetsTargetId = null;
				}
				$.design.locked.unAlign=false;
				//transfer temp var to real ones
				if (tempAlignTargetsTargetId) {
					$.design.alignTargets[targetId] = tempAlignTargetsTargetId;
				} else {delete $.design.alignTargets[targetId];}
			});
			
		 	return toReturn;
		 };
        
        /**
         * 	remove the son and align if needed
		 */ 
        $.fn.removeSon = function(son) {
        	var toReturn = $(this);
        	this.each(function() { 
        		son.remove();
        		$(this).css('height','auto');
        		if(!($.design.browser.fixedSupport)){
        			if($.design.alignTargets[$(this).attr("id")]) {
        				$(this).align($.design.alignTargets[$(this).attr("id")].options);
        			}
        		}
        	}); 
        	return toReturn;
    	};
    	 /**
         * 	add the son and align if needed
		 */ 
        $.fn.addSon = function(son) {
        	var toReturn = $(this);
        	this.each(function() { 
        		son.appendTo(toReturn);
        		$(this).css('height','auto');	
        		if(!($.design.browser.fixedSupport)){
        			if($.design.alignTargets[$(this).attr("id")]) {
        				$(this).align($.design.alignTargets[$(this).attr("id")].options);
        			}
        		}
        		$(window).resize();
        	}); 
        	return toReturn;
    	};
        /**
         * 	toggle the display of elements (including the 'hidden' class toggling)
		 */ 
        $.fn.toggle = function()
        {
        	return this.each(function() { 
	    		if(!$(this).is(':visible')) {
	    			$(this).removeClass("hidden");	//just in case
	    			$(this).fadeIn(60);
	    		} else	{$(this).fadeOut(60);}
        	}); 
    	};

    	 /**
         * 	connect a li to a div (given the id) as a submenu, possibility to give Class added when hover and class(es) added when out
         * ex : 
         * $("#myNote li").setSubMenu('myNoteDetail'});
         * $("#myNote li").setSubMenu({id:'myNoteDetail', hover:"hover", out:'bkgColor truc'});
		 */ 
        $.fn.setSubMenu = function(options) {
        	if (typeof options == "string") { options = {id: options}; }
        	var defaults = {id: null,  
        		hover: "hover", 
        		out:null, 
        		closeFunction : function(me){me.addClass("hidden");}, 
				keepOpen : false,
	    		openFunction : function(me){me.removeClass("hidden");}, 
	    		action:$.design.defaultAction};  
        	var options = $.extend(defaults, options);  
        	return this.each(function() { 
        		var li = $(this);
	    		var ul = li.parent();
	    		var sub = $("#"+options.id);
	    		//in case ul or li this don't have id
	    		var liId = li.getNotNullId();
				var ulId = ul.getNotNullId();
				if ($.design.menu[ulId]==null)
	    		{	//first time we add a sub to this ul
	    			$.design.menu[ulId] = new Array();
	    		}
	    		//connect
	    		$.design.menu[ulId][liId]={
	    			sub:sub, 
	    			options:{
						ulId:ulId, 
						sub:sub, 
						hoverClass:options.hover, 
						outClass:options.out,
						closeFunction:options.closeFunction,
						openFunction:options.openFunction, 
						action:options.action, 
						keepOpen : options.keepOpen}
					};
				$.design.menu[ulId].action = options.action;
				sub.attr("ul", ulId);
	    		sub.attr("li", liId);
				li.attr('menuItem', 1);
	    		if(options.action=="over")
	    		{	//if the event is when the mouse is over the menu
		    		li.hoverIntent({    
		    			sensitivity: 7,
		    			interval: 0, 
		    			timeout: 300, 
		    			over:function(){
		    				var li= $(this);
		    				var liId = li.attr('id');
		    				var ul = li.parent();
		    				var ulId = ul.attr('id');
		    				var mySub = $.design.menu[ulId][liId].sub;
		    				if(ul.attr("actif")=="1") {
		    					ul.pause();
		    					li.showSubMenu({
									li: li,
									liId: liId,
									ul: ul,
									ulId: ulId,
									options: $.design.menu[ulId][liId].options
								});
		    				} else {
		    					setTimeout(function(){
		    						ul.pause();
		    						li.showSubMenu({
										li: li,
										liId: liId,
										ul: ul,
										ulId: ulId,
										options: $.design.menu[ulId][liId].options
									});}, 400);
		    				}
		    			},
		    			out: function(){
		    				var li= $(this);
		    				var liId = li.attr('id');
		    				var ul = li.parent();
		    				var ulId = ul.attr('id');
		    				var sub = $.design.menu[ulId][liId].sub;
		    				if(sub.attr("actif")!="1")
		    				{
		    					if(li.attr("forced")=="1") {	  	
		    						ul.play();
			    				} else if(options.keepOpen==false) {			
			    					li.removeAttr("hover");
			    					li.removeClass(options.hover);
			    					//li.removeClass(options.hover[0]);
			    					if(options.out){li.addClass(options.out);}
									if(options.keepOpen==false){options.closeFunction(sub);}
			    				}
			    			}
		    			}
		    		});
		    		if($.browser.msie){
		    			//on ie the hover of links bloc focus
		    			sub.find('a').mouseenter(function() {
			    			$("#"+options.id).attr("actif", "1");
			    		}); 
		    		}	
			    	sub.hoverIntent({    
			    			sensitivity: 7, 
			    			interval: 0, 
			    			timeout: 500, 
			    			over:function(){
					    		var ulId = $(this).attr("ul");
			    				var ul = $("#"+ulId);
			    				ul.pause();
			    				$(this).attr("actif", "1");
			    			},
			    			out: function(){
			    				var ulId = $(this).attr("ul");
			    				var ul = $("#"+ulId);
			    				var liId = $(this).attr("li");
			    				var li = $("#"+liId);
			    				if(ul.attr("actif")!="1") {
			    					if(li.attr("forced")=="1") {ul.play();} 
			    					else if(options.keepOpen==false) {li.closeSubMenu($.design.menu[ulId][liId].options);}
			    				}
			    			}
			    		});
			    	ul.hoverIntent({    
		    			sensitivity: 7, 
		    			interval: 100, 
		    			timeout: 300, 
		    			over:function(){$(this).attr("actif", "1");},
		    			out:function(){$(this).attr("actif", "0");}
		    		});
	    		} else if(options.action=="click") {
	    			var liLink = li.find("a:first"); 
	    			liLink.live("click", function(){
	    					var li= $(this).closest("li");
		    				var liId = li.attr('id');
		    				var ul = li.parent();
		    				var ulId = ul.attr('id');
		    				var mySub = $.design.menu[ulId][liId].sub;
		    				if($.design.menu[ulId][liId].modulo == undefined){
		    					$.design.menu[ulId][liId].modulo = 3;	//each modulo we close/open
		    					if ($(this).attr("href")=='') {
		    						$.design.menu[ulId][liId].modulo=2;	//and if the menu link go to somewhere we firstclick: open,  second click : go to the link (it can be open with target="_blank", third click - close
		    					} 
		    				}
		    				var nbClicks = li.attr("nbClicks");
		    				if((nbClicks==undefined)||(sub.attr("actif")==0)){nbClicks=0;} //init nbClicks if first click since focus
		    				nbClicks = (parseInt(nbClicks)+1) % $.design.menu[ulId][liId].modulo;
		    				li.attr("nbClicks", nbClicks);
							if(nbClicks==1) {
		    					//open
		    					ul.attr("actif","1");
		    					ul.pause();
		    					li.showSubMenu({
									li: li,
									liId: liId,
									ul: ul,
									ulId: ulId,
									options: $.design.menu[ulId][liId].options
								});
		    					return false;
		    				}
		    				if (nbClicks==0) {
		    					//close
		    					if(li.attr("forced")=="1") {ul.play();} 
		    					else {
			    					if(options.keepOpen==true) {
										li.attr("nbClicks", 1);	//keep open
									} else {
										ul.attr("actif","0");	
										li.removeAttr("hover");
				    					li.removeClass(options.hover);
				    					if(options.out){li.addClass(options.out);}
				    					options.closeFunction(sub);
									}
			    				} 
								return false;
		    				}
		    			});
	    			}
        		}); 
    	};
    	
    	/**
	     * Can use to a li or ul, add the hoverClass to the li (/the first li of the ul),remove it from brothers li,  and show submenu if it has
	     * param : forceopen = true or false (will stay opened or not)
	     */
	  $.fn.openMenu = function(options) {
		  var defaults = {forced: false};  
		  var options = $.extend(defaults, options);  
	      return this.each(function() { 
		   		if($(this).attr("nodeName").toLowerCase()=="ul"){
					$(this).openNextMenu({forced:true});
				} else { //li
					$(this).attr('forced',"1");
					$(this).showSubMenu();
				}	
			});
	    };
	    /**
	     * Can use to a ul or li, add the hoverClass to the li (/the first li of the ul),remove it from brothers li,  and show submenu if it has
	     */
	    $.fn.openNextMenu = function(options) {
	    	return this.each(function() {
			var ul = $(this);
			if ($(this).attr("nodeName").toLowerCase() == "li") {ul = $(this).parent();}
			var lis = ul.children('li[menuItem]');
			var selectedLi = lis.filter('[hover]');
			if (selectedLi.length == 0) {var nextLi = lis.first();}
			else {
			  var nextLi = lis.filter('[hover]~li').first();
			  if(nextLi.length ==0) {nextLi = lis.first();}
			 }
			 if(options && options.forced==true) {nextLi.attr('forced',"1");}
			 nextLi.showSubMenu();
		    });
	    };
		 /**
	     * Can use to a li or ul, add the hoverClass to the li (/the first li of the ul),remove it from brothers li,  and show submenu if it has
	     */
	    $.fn.openPrevMenu = function() {
	    	return this.each(function() {
				var ul = $(this);
				if ($(this).attr("nodeName").toLowerCase() == "li") {ul = $(this).parent();}
			  	var lis = ul.children('li[menuItem]');
			 	var selectedLi = lis.filter('[hover]');
			  	if (selectedLi.length == 0) {var prevLi = lis.last();}
			  	else {
				  	var prevLi = selectedLi.prevAll('[menuItem]').last();
				  	if(prevLi.length ==0) {prevLi = lis.last();}
			  	}
			  	prevLi.openMenu({forced:false});
		    });
	    };
	    $.fn.play = function(options) {     	
			return this.each(function() { 
				var me = $(this);
			   	var myId = me.attr('id');
			   	if($.design.menu[myId]==undefined) {return;} //this is not a menu
			   	if($.design.menu[myId].options) {
			   		$.design.menu[myId].options.flip = options ? options : $.design.menu[myId].options.flip;
			   	} else {
			   		$.design.menu[myId].options = {flip : options ? options : 3000, playing:false};
			   	}
			   	if(!$.design.menu[myId].options.playing){
					me.openMenu({forced:true});
					$.design.menu[myId].options.playing=true;
				}
			   clearTimeout($.design.menu[myId].timer);
			   $.design.menu[myId].timer = setInterval(function(){me.openNextMenu({forced:true});}, $.design.menu[myId].options.flip);});
	    };
		$.fn.pause = function() { 
		   return this.each(function() { 
				   var me = $(this);
				   if($.design.menu[me.attr('id')] && $.design.menu[me.attr('id')].timer) {
					   clearTimeout($.design.menu[me.attr('id')].timer);
				   }
			});   
	    };
	    $.fn.stop = function() {$(this).closeMenu();};
	    $.fn.closeMenu = function() {
	    	return this.each(function() { 
		    	var target = null;
		    	if($(this).attr("nodeName").toLowerCase()=="ul"){
		    		var ulId = $(this).getNotNullId();
		    		target = $(this).find('li[hover]');
					if($.design.menu[ulId] && $.design.menu[ulId].timer) {
						clearTimeout($.design.menu[ulId].timer);
					}
					//menu is no more playing
					$.design.menu[ulId].options.playing=false;
		    	} else {target = $(this);}
			    target.attr("forced",'0');
		    	target.closeSubMenu(null);
		    });
	    };
    	 /**
	     * Can use to a li, parameters are hused for intern use, if manual show, just don't add parameter
	     */
	    $.fn.showSubMenu = function(options) {
			if(!options) {
				options = [];
				options.li= $(this);
				options.liId = options.li.getNotNullId();
				options.ul = options.li.parent();
				options.ulId = options.ul.getNotNullId();
		    	options.options = $.design.menu[options.ulId][options.liId].options;  
			}
	    	if((options.ul.attr("actif")=="1")||(options.li.attr("forced")=="1")) {      		
	      		var oldli = options.ul.children('[hover]');
	    		if(oldli.length>0) {
					//close old Li
					var oldliID = oldli.attr("id");
					if(oldliID != options.liId) {
	    				//if oldLi != li => transfert le forced
						options.li.attr("forced",oldli.attr("forced"));
	    				oldli.attr("forced", "0");
						oldli.removeAttr("hover");
						oldli.closeSubMenu($.design.menu[options.ulId][oldliID].options);
	    			}
				}
				
	    		//show the new one
	    		options.li.addClass(options.options.hoverClass);
	    		if(options.options.outClass){options.li.removeClass(options.options.outClass);}
	      		options.li.attr("hover", '1');
	      		if(options.options.action=="click") {
	      			options.options.sub.attr("actif", '1');
	      			options.li.attr("nbClicks", '1');
	      		}
	      		options.options.openFunction(options.options.sub);
	    	}
	    };
	    
	    /**
	     * Can use to a li, parameters are here to speed it up
	     */
	    $.fn.closeSubMenu = function(options) {
	    	return this.each(function() { 
	    		if($(this).attr("forced")!="1") {
			    	if(options ==null) {
			    		var ul=$(this).parent();
			    		options = $.design.menu[ul.attr('id')][$(this).attr("id")].options;    
			    	}
			    	
			    	if(options !=null) {
			    		var li = $(this);
			    		if(options.action=="click") {li.attr("nbClicks", '0');}
			    		li.removeAttr("hover");
			    		var sub = $.design.menu[options.ulId][li.attr('id')].sub;
			    		li.removeClass(options.hoverClass);
			    		
						if(options.outClass){li.addClass(options.outClass);}
						options.closeFunction(sub);
						sub.attr("actif", '0');    	
				    }
				}
			});
	    };
	    $.fn.setPosition = function(options) {
			if(options==null || typeof options == "string") {options = {position:options, offset:[]};}
			var defaults = {position: "absolute", offset:[]};  
			var options = $.extend(defaults, options);  
		    
				return this.each(function() { 
		    	var me = $(this);
		    	var myId = me.getNotNullId();	
				if (options.position == null && $.design.ghosts[myId]) {
		    		if ($.design.alignTargets[myId]) {
		    			me.unAlign($.design.alignTargets[myId].options);
		    		}
		    		me.createGhost(false);
		    	} else {
		    		var myCoordinates = me.coordinates();
		    		if (!$.design.ghosts[myId]) {
		    			me.createGhost(true);
		    			me = $("#"+myId);
		    		}
		    		//default values for "fixed"
		    		var frameOfReferenceId = "";
		    		var myOffset = {left:myCoordinates.left, top:myCoordinates.top};
		    		if (options.position=="absolute") {
		    			var dad = me.parent();
		    			frameOfReferenceId = dad.getNotNullId();
		    			myCoordinates = dad.coordinatesOf(myCoordinates);
		    			myOffset =  {left:myCoordinates.left, top:myCoordinates.top};	
		    		}
		    		//add parameters offsets
		    		myOffset.left = options.offset.left ? myOffset.left + options.offset.left : options.offset.right ? myOffset.left - options.offset.right : myOffset.left;
		    		myOffset.top = options.offset.top ? myOffset.top + options.offset.top : options.offset.bottom ? myOffset.top - options.offset.bottom : myOffset.top;
		    		
		    		me.align({left:frameOfReferenceId, top:frameOfReferenceId, offset : myOffset});
		    	}
	    		
			});
	    };
	    
	    $.fn.createGhost = function(options) {return this._executeCreateGhost(options);};
    	/**
		createGhost("fixed") : fix the element on the screen
		createGhost("absolute") : fix the element on the page
		createGhost(null) : set back the element at his place
		 */ 
	    $.fn._executeCreateGhost = function(options) {
	    	var toReturn = null;
	    	this.each(function() {  
	    		var me = $(this); toReturn = me;
				var myId = me.getNotNullId();		
				$.design.locked.createGhost = true;
				if(options && !me.hasClass("ghost") && ($.design.ghosts[myId] == undefined || $.design.ghosts[myId] == null)) {	
					//we are going to create ghost 
	    			var ghostContainer = $("#ghostContainer");
	    			if(ghostContainer.length==0) {
						//if first call, create ghost container	
						$("body").append('<div class="absolute tCenter" style="width:100%;"><div id="ghostContainer" class="relative center siteWidth tLeft"></div></div>');
	    				ghostContainer = $("#ghostContainer");
	    			}
					//first time we move the element : create ghost
					//transfert ghost and me
					var myCoordinates = me.coordinates();
					me.css({width:myCoordinates.width, height:myCoordinates.height});
					var futureMe = me.clone();
					futureMe.attr("id", myId);
					futureMe.html('');
					if (!futureMe.hasClass("invisible")) {futureMe.addClass("invisible");}
	    			futureMe.insertBefore(me);
	    			ghostContainer.prepend(me);
	    			var ghostId = 'Ghost-'+myId;
    				me.attr('id', ghostId);
	    			ghost = me;
					me = futureMe;
					toReturn = futureMe;
	    			ghost.addClass("ghost");
					$.design.ghosts[myId] = ghostId;	
	    		} else if(!options && ($.design.ghosts[myId] != null && $.design.ghosts[myId] != undefined)) {
	    			//the ghost exist we are deleting it now
	    			if (me.hasClass('invisible')) {me.removeClass('invisible');}
					var ghost = $("#"+$.design.ghosts[myId]);
					ghost.attr("id", myId);
					ghost.attr("class", me.attr("class"));
					ghost.attr("style", me.attr("style"));
					ghost.insertBefore(me);
					me.remove();
					me=ghost;
					toReturn = me;
					delete ghost;
					delete $.design.ghosts[myId];
	    		}	
	    	});
			$.design.locked.createGhost = false;
	    	return toReturn;
	    };	
		
	    /**
	     create Message to the element 
	     	if parameter = just a string, this is considered as the message content
	     	- options.position is the same array given to align function ex : {top: "#blop"	,  right: "#blop"	,  bottom: "#blop"	,  left: "#blop"	}
	     		- to specify the target as a position, put 'this' ex : top:'this'
	     	- width : the width (default 300px)
	     	- class = the class added to the message (default : bkgMedium) 
	     	- content : the html of the message
	     	- lifeTime : miliseconds of life when the mouse is not on the message
	     */
	    $.fn.createMessage = function(options) {
	    	if (typeof options == "string") {options = {content: options};  }
	    	var defaults = {position:null, width : '200px', messageClass : 'margin bkgDarker edit', content : 'this is a message', lifeTime : null };
	    	options = $.extend(defaults, options);  
   			return this.each(function() { 
   				var me = $(this);
   				if(me.attr("message")==null) {
	   				var myId = me.getNotNullId();
					var messageId = 'message-'+myId;
		    		var myClass='class="wAuto"';
		    		if(options.width) {myClass='';}
		    		$("body").append('<div id="'+messageId+'"'+myClass+' style="overflow:visible;" ><div style="width:'+options.width+'" class="'+options.messageClass+'">'+options.content+'</div></div>');
					var message = $("#"+messageId);
					message.css("width", message.children(":first").outerWidth());
					//message = message.createGhost(true);
					me.attr('message', messageId);
					var myPosition = new Array();
					if(!options.position) {
						//default align on the right of me
						myPosition = {leftIsRightOf : myId, top:myId};
					} else {
						for (x in options.position) {//replace 'this' by the good id
							if(options.position[x]=='this') {myPosition[x] = myId;} else {myPosition[x] = options.position[x]; }
						}
					}
					
					if(options.lifeTime) {
						$.design.timers[myId] = setTimeout(function(){me.deleteMessage();}, options.lifeTime);
						$("#"+$.design.ghosts[messageId]).hoverIntent({    
			    			sensitivity: 7,
			    			interval: 100, 
			    			timeout: options.lifeTime, 
			    			over:function(){
			    				clearTimeout($.design.timers[myId]);	
								delete $.design.timers[myId];
			    			},
			    			out : function() {
			    				$.design.timers[myId] = setTimeout(function(){me.deleteMessage();}, options.lifeTime);
			    			}
		    			});
					}
					message.align(myPosition);
					
				}
			});
		};
		/**
	     delete message of target element 
	     */
	    $.fn.deleteMessage = function() {
	    	return this.each(function() { 
   				var me = $(this);
   				var messageId = me.attr("message");
   				if(messageId) {
   					var myId = me.attr("id");
   					me.removeAttr('message');
	   				var message = $("#"+messageId);
	   				message.unAlign($.design.alignTargets[messageId].options);
	   				message = $("#"+messageId);
	   				//delete timer
	   				clearTimeout($.design.timers[myId]);	
					delete $.design.timers[myId];
	   				message.empty().remove();
				}
			});
	    };
})(jQuery);

/** do init the plugin */
$.design.init();