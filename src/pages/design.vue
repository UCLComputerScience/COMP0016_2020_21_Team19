<template>
  <div>
    <PageTitle title="Design"></PageTitle>
      <!--Implantation of finished functionality-->
      <section class="section">
          <div class="container">
              <div class="row">
                  <div class="col-lg-10 mx-auto text-center">
                      <h3 class="section-title">Tech Stack & Implementation</h3>

                      <div class="text-left">
                          <br />
                          <br />

                          <h4>Django</h4>
                          <p>
                          Activity League has been developed using Django. Django proved to be a very good choice for the development of our web app, as it handled standard cases of functionalities
                          that would need to be implemented in our platform by default (for example, the creation and validation of forms). Moreover, Django has its own ORM (Object-Relational Mapper) which completely
                          handles the relationship between the classes that we defined as our project and the relations in our PostgreSQL database.
                          <br><br>
                          Activity League has been programmed to follow Django's file-structure convention and default Model View Controller implementation. Django breaks down a project into applications. Each 
                          generated application has a models.py file containing the classes to be used in that application (translated to relations in the database by the ORM), a views.py file containing view functions
                          which map web requests to web responses and plenty of flexibility when writing control logic. For each app that we defined in the project, we created a utils.py file containing the vast majoroity
                          of the logic and utility functions associated with each of our view functions.
                          <br><br>
                          Applications that are involved with pages that create and submit forms, such as the new task page and pages allowing you to add/remove people from groups and organisations also have a dedicated
                          forms.py file. This file leverages the existing Django Forms API and contains the structure and content of the forms that are used in each of these views.
                          <br><br>
                          </p>
                          <p>
                              <carousel :perPage="1" :navigationEnabled="true" style="text-align: center">
                                  <slide v-for="n in 9" v-bind:key="n">
                                      <img :src="'images/' + n + '.png'" class="img-responsive slideImg">
                                  </slide>
                              </carousel>
                          </p>
                          
                          <br><br>
                          <h4>Database</h4>
                          <p>
                          The backend of Activity League rests on PostgreSQL databases. PostgreSQL was a particularly suitable choice for Activity League, given there was extensive literature and resources available on
                          the Django documentation on integrating the two of them. Our data also fit the relational model very nicely given the structure of our data, and the fact that lots of the functionalities required
                          could be implemented using small, structured SQL queries. Conveniently, PostgreSQL was also free. This stands in contrast to other popular databases including MongoDB, which was paid.
ites 
                        
                          <br><br>
                          As mentioned in the previous section, Django's ORM handled the translation between models (classes) defined specific to Activity League to tables, where one model defined corresponded to one table.
                          <br><br>r>
                          <carousel :perPage="1" :navigationEnabled="true" style="text-align: center">
                              <slide v-for="n in 12" v-bind:key="n">
                                  <img :src="'images/' + n + '.png'" class="img-responsive slideImg">
                              </slide>
                          </carousel>
                          <br>
                          <p>
                              We have hosted our backend on Azure B1s virtual machine at a cost of £6.42 per month, provided by UCL. In order to efficiently manage the backend server, I have set up
                              a github webhook in our server, in order to automatically pull and deploy the latest github changes.
                          </p>
                          <br><br>
                          <h4>Docker</h4>
                          <p>
                          To ensure the easy deployment of Activity League, we decided to dockerise the entire application. Docker is a containerisation service - allowing for software to be distributed in the form of
                          packages called containers. Containers allowed developers to isolate the development of an app from its local environment. This is particularly useful in deployment, as it means that theoretically,
                          any system with docker installed could simply pull the Activity League container and run it on their system without dependency version conflicts (dependencies and versions are specified in the container).
                          <br><br>
                          Given Activity League was going to be deployed on a Linode server, Docker's containerisation system also likely saved a great amount of time debugging features that worked locally but didn't work on the
                          server, which allowed us to further refine and implement new functionalities to our solution.
                          <br><br>
                          <carousel :perPage="3" :navigationEnabled="true" style="text-align: center">
                              <slide v-for="n in 11" v-bind:key="n">
                                  <img :src="'images/' + n + '.jpeg'" class="img-responsive slideImg">
                              </slide>
                          </carousel>
                          </p>
                          <br><br>
                          <h4>Linode</h4>
                          <carousel :perPage="1" :navigationEnabled="true" style="text-align: center">
                              <slide v-for="n in 15" v-bind:key="n">
                                  <img :src="'images/' + n + '.jpeg'" class="img-responsive slideImg">
                              </slide>
                          </carousel>
                          <p>
                          Activity League is currently deployed on a Linode server with 1 core, 1GB of RAM and 25GB of storage for a total cost of $5 per month. Linode was selected out of client preference, but was a convenient choice
                          for the project deployment given its simplicity to setup.
                          <br><br>
                          As part of a continuous deployment practice, Activity League makes use of <a href="https://github.com/containrrr/watchtower" target="_blank">WatchTower</a> on the Linode server. Every time a new commits is made to the the main branch, GitHub actions runs our
                          tests and if they pass, builds a new Docker image hosted on GitHub packages, which WatchTower looks for. WatchTower is configured to probe the project repository every 60 seconds, and if it detects a newer edition of the image being hosted by GitHub packages,
                          it takes the old version down and deploys the new image automatically.
                          <br><br>
                          The database state is separate from this image - it is a persistent volume stored on the Linode server, meaning that we can continue merging pull requests in the main repository (assuming there were no changes to the structure of the database)
                          without having to repopulate the database each time that it was built. Hence, each time that we pushed to the main branch, we would see the latest version of the app deployed to the server in under two minutes.
                          <br><br>
                          </p>
                          <p>We used Vue a progressive javascript framework for web application development together with the Material design which backed by Google. Vue using latest design structure MVVM to keep track of data, if the data changes the view will also update to the corresponding layout.

                              The web application is responsive means it can optimize its layout in different size of the screen, and the design when running on mobile models tend to be like a native application rather than a web application.

                              User can log in or register on the web application. Once login, user can modify their detail such as choosing AR model, upload image as profile and filling the detail. The history and favourite list are up to date with the mobile application. User can delete or view the detail of each item from the list.</p>
                          <br><br>
                      </div>
                  </div>
              </div>



          </div>
      </section>
      <!--/Implentation of finished functionality-->

    <!--System Arthitecture Diagram-->
    <section class="section">
      <div class="container">
        <div class="row">
          <div class="col-lg-10 mx-auto text-center">
            <h3 class="section-title">System Architecture Diagram</h3>
            <img src="images/" class="img-responsive" style="width: 100%;" />
              *We have decided to use JWT authentication instead of LinkedIn OAuth, however this can be added in the future.
          </div>
        </div>
      </div>
    </section>
    <!-- /System Arthitecture Diagram-->

      <section class="section">
          <div class="container">
              <div class="row">
                  <div class="col-lg-10 mx-auto text-center">
                      <h3 class="section-title">User Sequence Diagram</h3>
                      <carousel :perPage="1" :navigationEnabled="true" style="text-align: center">
                            <slide v-for="n in 6" v-bind:key="n">
                                <img :src="'images/design/sequence/' + n + '.png'" class="img-responsive slideImg">
                            </slide>
                        </carousel>
                      <p class="text-left">LOREM IPSUM</p>
                  </div>
              </div>
          </div>
      </section>

      <section class="section">
          <div class="container">
              <div class="row">
                  <div class="col-lg-10 mx-auto text-center">
                      <h3 class="section-title">User Authentication Sequence Diagram</h3>
                      <img src="images/design/signup.png" class="img-responsive" style="width: 70%;" />
                  </div>
              </div>
          </div>
      </section>


      <section class="section">
          <div class="container">
              <div class="row">
                  <div class="col-lg-10 mx-auto text-center">
                      <h3 class="section-title">Data Storage ER Diagram</h3>
                      <img src="images/" class="img-responsive" style="width: 100%;" />
                  </div>
              </div>
          </div>
      </section>



    <!--ER Diagram-->
    <section class="section">
      <div class="container">
        <div class="row">
          <div class="col-lg-10 mx-auto text-center">
            <h3 class="section-title">Class Diagrams (Entity Relationship)</h3>
              <div class="class-diagram">
                <h4>Overall</h4>
                <SvgPanZoom
                        style="width: 100%; height: 600px; "
                        :zoomEnabled="true"
                        :controlIconsEnabled="true"
                        :fit="true"
                        :center="true"
                        :contain="true"
                >
                  <svg width="100%" height="600px"><image x="0" y="0" width="100%" height="100%" xlink:href="images/design/overall.svg" /></svg>
                </SvgPanZoom>
                <br>Use mouse to pan, double tap to zoom.
              </div>

              <hr>
              <div class="class-diagram">
                  <h4>Backend App (Node.JS)</h4>
                  <carousel :perPage="1" :navigationEnabled="true">
                      <slide v-for="n in 6" v-bind:key="n">
                          <img :src="'images/design/node/'+n+'.png'" class="img-responsive slideImg">
                      </slide>
                  </carousel>
              </div>

          </div>
        </div>
      </div>
    </section>
    <!-- /ER Diagram-->








  </div>
</template>

<script>
import PageTitle from "../components/PageTitle.vue";
import SvgPanZoom from 'vue-svg-pan-zoom';
import { Carousel, Slide } from 'vue-carousel';
export default {
  name: "design",
  components: {
    PageTitle,
    SvgPanZoom,
    Carousel,
    Slide
  }
};
</script>

<style scoped>
    .class-diagram{
        margin-top: 50px;
        margin-bottom: 50px;
    }
    .slideImg{
        max-height: 500px;
        max-width: 100%;
    }
</style>