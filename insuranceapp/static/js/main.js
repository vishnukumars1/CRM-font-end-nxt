function animateCounters() { 
    const counters = 
        document 
            .querySelectorAll(".counter"); 
    counters 
        .forEach((counter, index) => { 
            const target = 
                parseInt(counter 
                    .getAttribute( 
                        "data-target") 
                ); 
            const duration = 1000; 
            const step = 
                Math.ceil( 
                    (target / duration) * 15 
                ); 
            let current = 0; 
  
            const updateCounter = () => { 
                current += step; 
                if (current <= target) { 
                    counter 
                        .innerText = current; 
                    requestAnimationFrame(updateCounter); 
                } else { 
                    counter.innerText = target; 
                } 
            }; 
  
            setTimeout(() => { 
                updateCounter(); 
            }, index * 1000); 
            // Delay each counter by 1 second 
        }); 
} 
  
animateCounters();

(function ($) {
    "use strict";

    new WOW().init();
    
    })(jQuery);