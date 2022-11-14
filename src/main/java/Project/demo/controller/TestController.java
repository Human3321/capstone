package Project.demo.controller;


import Project.demo.DTO.TestDTO;
import Project.demo.service.TestService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequiredArgsConstructor
public class TestController {
    private final TestService testService;
    @RequestMapping(value = "/",method = RequestMethod.GET)
    public Object test()
    {
        return "Hello";
    }

    @RequestMapping(value = "/user", method = RequestMethod.GET)
    public List<TestDTO> getUser()
    {
        return testService.getUserList();
    }

}
