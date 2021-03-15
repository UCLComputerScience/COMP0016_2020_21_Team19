<template>
  <div>
    <PageTitle title="Design"></PageTitle>
      <!-- Tech Stack and Implementation -->
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
                          Activity League has been programmed to follow Django's file-structure convention and default Model View Template implementation. Django breaks down a project into applications. Each 
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
                                  <slide v-for="n in 6" v-bind:key="n">
                                      <img :src="'images/design/django/' + n + '.png'" class="img-responsive slideImg">
                                  </slide>
                              </carousel>
                          </p>

                          <h4>Bootstrap</h4>
                          <p>
                          To ensure that our application was responsive to changes in the screen size and devices using it, we used the frontend framework Bootstrap when creating our HTML templates.
                          Consequently, the web application is optimised for specific devices when using it. For example, logging in to Activity League on an iPhone will hide our sidebar menu and
                          open it on click, with a smooth transition animation, whereas when viewed on desktop, it remains stuck to the left hand side of the page.
                          <br><br>
                          This was an important consideration for us, given that our dashboard is feature and content heavy, and without the ability to restyle the layout by device, our web app 
                          would have been virtually unusable on smaller devices.
                          <br><br>
                          </p>
                          <p>
                              <carousel :perPage="1" :navigationEnabled="true" style="text-align: center">
                                  <slide v-for="n in 3" v-bind:key="n">
                                      <img :src="'images/design/bootstrap/' + n + '.png'" class="img-responsive slideImg">
                                  </slide>
                              </carousel>
                          </p>
                          
                          <br><br>
                          <h4>Database</h4>
                          <p>
                          All data stored by Activity League lies in a PostgreSQL database. PostgreSQL was a particularly suitable choice for Activity League, given there was extensive literature and resources available on
                          the Django documentation on integrating the two of them. Our data also fit the relational model very nicely given the structure of our data, and the fact that lots of the functionalities required
                          could be implemented using small, structured SQL queries. Conveniently, PostgreSQL was also open source. This stands in contrast to other popular databases including MongoDB, which was a paid alternative.
                        
                          <br><br>
                          As mentioned in the previous section, Django's ORM handled the translation between models (classes) defined specific to Activity League to PostgreSQL tables, where one model defined corresponded to one table.
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
                          <img src="images/design/docker.png" class="img-responsive" style="width: 100%;">
                          </p>
                          <br><br>

                          <h4>Linode</h4>
                          <img src="images/design/linode.png" class="img-responsive" style="width: 100%;">
                          <p>
                          Activity League is currently deployed on a Linode server with 1 core, 1GB of RAM and 25GB of storage for a total cost of $5 per month. Linode was selected out of client preference, but was a convenient choice
                          for the project deployment given its simplicity to setup.
                          <br><br>
                          As part of a continuous deployment practice, Activity League makes use of <a href="https://github.com/containrrr/watchtower" target="_blank">WatchTower</a> on the Linode server. Every time a new commits is made to the the main branch, GitHub Actions runs our
                          tests and if they pass, builds a new Docker image hosted on GitHub packages, which WatchTower looks for. WatchTower is configured to probe the project repository every 60 seconds, and if it detects a newer edition of the image being hosted by GitHub Packages,
                          it takes the old version down and deploys the new image automatically.
                          <br><br>
                          The database state is separate from this image - it is a persistent volume stored on the Linode server, meaning that we can continue merging pull requests in the main repository (assuming there were no changes to the structure of the database)
                          without having to repopulate the database each time that it was built. Hence, each time that we pushed to the main branch, we would see the latest version of the app deployed to the server in under two minutes.
                          <br><br>
                          </p>
                          <br><br>
                      </div>
                  </div>
              </div>
          </div>
      </section>
      <!--/Tech Stack and Implementation-->

    <!--Design Patterns-->
    <section class="section">
      <div class="container">
        <div class="row">
          <div class="col-lg-10 mx-auto text-center">
            <h3 class="section-title">Design Patterns</h3>
            <div class="text-left">
            <!-- MVT -->
            <h4>Model View Template</h4>
            <p>
            By default, Django formats its files in accordance with the principles of the MVT design pattern (each application have models.py, views.py and template files associated with them). Our solution has been developed
            in extension of thes principles which nicely decouples the templates from the views, subsequently making editing specific pages a lot easier.
            <br><br>
            The design pattern is very similar to the Model View Controller pattern, which separates the models from the views with the controller (housing all of the control logic) as the middle man. This design pattern was
            an option that we considered given it would have made the flow easier to understand. However, we decided that the MVT template was the optimal choice as the controller is managed by Django itself (controlling The
            interactions between the models and the view), making an additional implementation unnecessary.
            <br><br>
            MVT allows Activity League to be easily scalable: the addition of a new page simply requires the creation of a new template, a URL being added and a single function being written within the application to render
            the newly defined template. We hope that in future, our design choice here significantly speeds the process by which developers may add new pages and functionalities to Activity League.
            <br><br>
            </p>
            <!-- /MVT -->

            <!-- Adapter -->
            <h4>Adapter</h4>
            <p>
            During the invitation processs (by email), Activity League uses two dependencies: django-invitations (takes care of the email invitations) and django-allauth (takes care of secure user authentication). As Activity
            League is invite-only and django-allauth doesn't support customisation of signup methods (signup is either closed or it isn't), we implemented the adapter design pattern to change the signal that was being passed
            from django-inviations to django-allauth. This allows us to selectively open the signup if a user is creating an organisation, but closes it off otherwise.
            </p>
            <!-- /Adapter --> 
            </div>
          </div>
        </div>
      </div>
    </section>
    <!-- /Design Patterns-->
    
    <!--System Arthitecture Diagram-->
    <section class="section">
      <div class="container">
        <div class="row">
          <div class="col-lg-10 mx-auto text-center">
            <h3 class="section-title">System Architecture Diagram</h3>
            <img src="images/design/architecture.png" class="img-responsive" style="width: 100%;" />
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

    <!--Entity Relationship Diagram-->
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
                  <h4>App-specific</h4>
                  <carousel :perPage="1" :navigationEnabled="true">
                      <slide v-for="n in 4" v-bind:key="n">
                          <img :src="'images/design/class-diagrams/' + n +'.png'" class="img-responsive slideImg">
                      </slide>
                  </carousel>
              </div>
          </div>
        </div>
      </div>
    </section>
    <!-- /Entity Relationship Diagram-->

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