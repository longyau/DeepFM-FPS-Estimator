package com.example.fpsestimator;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.servlet.ModelAndView;
@Controller
@RequestMapping("website")
public class WebPageController {
    public WebPageController(){
    }
	@CrossOrigin
	@RequestMapping(value = "/", method = RequestMethod.GET)
	public String home() {
		/*ModelAndView mvc=new ModelAndView();
		mvc.setViewName("main.html");
		return mvc;*/
		return "main.jsp";
	}
}
