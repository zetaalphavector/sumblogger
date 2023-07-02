## Concerns
- Order of `params_mapping` matters if the user wants to rename a field that has already given in a previous usecase
- no objects are allowed in the prompt templates, so if we want a list of document objects that contain doc id and content, we should create two template input variables: doc_ids, doc_contents which match one by one to each document
- when creating a TextCompletionClient, we cannot know if the usecase is compatible with the client at hand during build time. Instead, it will break during run time, so when we configure a usecase we should already know which types of text completion clients are supported (e.g. prompt_with_logits etc)
- the LLMConfig passed to the TextCompletionClient contains any kind of template that might be needed by any client. That results in having many optional fields like prompt_template, or bot_conversation. Each client should handle how it will use these fields and when it will raise an error. This error though will be triggered at runtime.

- The PromptParams contains arbitrary keys in the dictionary. In the general case of pass-through services, this is not such a problem since those keys are configured only in the usecase_configs and they do not appear in the code at all. When creating custom text completion services though, such as title_per_document, we might need to access specific keys from the PromptParams. The name of those are taken from the input variables of the usecase_config, but the connection is hidden. If somebody changes the field in the config or in the service, this will cause a bug. Can we prevent this? 
Could we define inherit from PromptParams and create a type custom-made for our service, where we can define the exact expected key? Could Protocols be used in this case?

- A response for `tools/experimentation/pipelines/multi_xscience_twostep.py` for 2 test data points of Multi-XScience is given below.

**Concern:** Do we actually want to allow list of PromptParams to be given in the input of a SingleUsecase and be executed in parallel?
Or is it better to just create a `ExecuteTextCompletionUsecases` parallel command and pass their a list of `ExecuteTextCompletionSingleUsecase` that we want to parallelize?
This would avoid creating lists of lists of lists like below. Only two-level lists would be created, cause parallelization would happen only in the Usecases command level and not in SingleUsecase command as well.
~~~
{
    "output_params_list": [
        {
            "ref_document_ids": [
                [["@cite_9", "@cite_15", "@cite_6", "@cite_8"]],
                [["@cite_21"]],
            ],
            "number_of_words": [[105], [105]],
            "generated_summaries": [
                [
                    "In the related work, several articles have been referenced that provide insights into the problem at hand. Smith et al. [@cite_8] propose a method for agents in economic Multi-Agent Systems to determine when to behave strategically and when to act as price-takers. They provide a framework for incremental implementation of modeling capabilities and investigate the behavior of different agent populations. Another article by the same authors [@cite_9] explores the implications of agent tracking capabilities for agent architectures in real-time and dynamic environments. Additionally, a study by Jones et al. [@cite_6] outlines a gradual evolution in the formal conception of intelligence, aiming to bridge the gap between theory and practice in AI research. Finally, an article by Brown [@cite_15] provides an introduction to a model using automobiles as an example and discusses examples, applications, and counteracting institutions."
                ],
                [
                    "The proposed grasping system in this work builds upon the hybrid approach presented in [@cite_21]. The previous work focuses on automating grasping movement in virtual actors using forward and inverse kinematics. It aims to generate realistic grasping motion for objects with arbitrary shapes. Our approach extends this idea by incorporating visually realistic hand fitting and user-controlled positioning and orientation using VR handheld controllers. By adapting the system to different hand meshes and enabling interaction with various object geometries, our approach offers flexibility and customization. The performance analysis conducted in this study validates the effectiveness of our proposal in providing an enjoyable and intuitive VR interaction experience."
                ],
            ],
            "single_doc_summaries": [
                [
                    [
                        "The referenced article explores the implications of agent tracking capabilities for agent architectures in real-time and dynamic environments, emphasizing the need for flexible and efficient reasoning about other agents' models.",
                        "The referenced article provides an introduction to a model using automobiles as an example, discusses examples and applications, explores counteracting institutions, and concludes with a summary.",
                        "This referenced article outlines a gradual evolution in the formal conception of intelligence, aiming to bridge the gap between theory and practice in AI research.",
                        "In their study, Smith et al. propose a method for agents in economic Multi-Agent Systems to determine when to behave strategically and when to act as price-takers, providing a framework for incremental implementation of modeling capabilities and investigating the behavior of different agent populations.",
                    ]
                ],
                [
                    [
                        "The referenced article proposes a hybrid approach using forward and inverse kinematics to automate grasping movement in virtual actors, with a focus on generating realistic grasping motion for arbitrary shaped objects."
                    ]
                ],
            ],
            "main_documents": [
                [
                    "We present our approach to the problem of how an agent, within an economic Multi-Agent System, can determine when it should behave strategically (i.e. learn and use models of other agents), and when it should act as a simple price-taker. We provide a framework for the incremental implementation of modeling capabilities in agents, and a description of the forms of knowledge required. The agents were implemented and different populations simulated in order to learn more about their behavior and the merits of using and learning agent models. Our results show, among other lessons, how savvy buyers can avoid being cheated'' by sellers, how price volatility can be used to quantitatively predict the benefits of deeper models, and how specific types of agent populations influence system behavior."
                ],
                [
                    "Abstract Interaction in virtual reality (VR) environments (e.g. grasping and manipulating virtual objects) is essential to ensure a pleasant and immersive experience. In this work, we propose a visually realistic, flexible and robust grasping system that enables real-time interactions in virtual environments. Resulting grasps are visually realistic because hand is automatically fitted to the object shape from a position and orientation determined by the user using the VR handheld controllers (e.g. Oculus Touch motion controllers). Our approach is flexible because it can be adapted to different hand meshes (e.g. human or robotic hands) and it is also easily customizable. Moreover, it enables interaction with different objects regardless their geometries. In order to validate our proposal, an exhaustive qualitative and quantitative performance analysis has been carried out. On one hand, qualitative evaluation was used in the assessment of abstract aspects, such as motor control, finger movement realism, and interaction realism. On the other hand, for the quantitative evaluation a novel metric has been proposed to visually analyze the performed grips. Performance analysis results indicate that previous experience with our grasping system is not a prerequisite for an enjoyable, natural and intuitive VR interaction experience."
                ],
            ],
            "ref_documents": [
                [
                    [
                        "In multi-agent environments, an intelligent agent often needs to interact with other individuals or groups of agents to achieve its goals. Agent tracking is one key capability required for intelligent interaction. It involves monitoring the observable actions of other agents and inferring their unobserved actions, plans, goals and behaviors. This article examines the implications of such an agent tracking capability for agent architectures. It specifically focuses on real-time and dynamic environments, where an intelligent agent is faced with the challenge of tracking the highly flexible mix of goal-driven and reactive behaviors of other agents, in real-time. The key implication is that an agent architecture needs to provide direct support for flexible and efficient reasoning about other agents' models. In this article, such support takes the form of an architectural capability to execute the other agent's models, enabling mental simulation of their behaviors. Other architectural requirements that follow include the capabilities for (pseudo-) simultaneous execution of multiple agent models, dynamic sharing and unsharing of multiple agent models and high bandwidth inter-model communication. We have implemented an agent architecture, an experimental variant of the Soar integrated architecture, that conforms to all of these requirements. Agents based on this architecture have been implemented to execute two different tasks in a real-time, dynamic, multi-agent domain. The article presents experimental results illustrating the agents' dynamic behavior.",
                        "I. Introduction, 488. — II. The model with automobiles as an example, 489. — III. Examples and applications, 492. — IV. Counteracting institutions, 499. — V. Conclusion, 500.",
                        "The long-term goal of our field is the creation and understanding of intelligence. Productive research in AI, both practical and theoretical, benefits from a notion of intelligence that is precise enough to allow the cumulative development of robust systems and general results. This paper outlines a gradual evolution in our formal conception of intelligence that brings it closer to our informal conception and simultaneously reduces the gap between theory and practice.",
                        "",
                    ]
                ],
                [
                    [
                        "Abstract This paper addresses the important issue of automating grasping movement in the animation of virtual actors, and presents a methodology and algorithm to generate realistic looking grasping motion of arbitrary shaped objects. A hybrid approach using both forward and inverse kinematics is proposed. A database of predefined body postures and hand trajectories are generalized to adapt to a specific grasp. The reachable space is divided into small subvolumes, which enables the construction of the database. The paper also addresses some common problems of articulated figure animation. A new approach for body positioning with kinematic constraints on both hands is described. An efficient and accurate manipulation of joint constraints is also presented. Finally, we describe an interpolation algorithm which interpolates between two postures of an articulated figure by moving the end effector along a specific trajectory and maintaining all the joint angles in the feasible range. Results are quite satisfactory, and some are shown in the paper."
                    ]
                ],
            ],
        }
    ]
}

~~~