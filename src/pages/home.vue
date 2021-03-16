<template>
  <div>
    <section class="hero-section" data-scroll-index="0">
      <div class="container h-100">
        <div class="row align-items-center h-100">
          <div class="col-lg-7 col-md-10 col-sm-12">
            <img
              src="images/logos.png"
              alt="logo image"
              style="max-width: 300px;padding-bottom: 20px"
            />
            <h1
              class="hero-section-title wow fadeInUp"
              data-wow-delay="0.2s"
            >Activity League</h1>
            <p class="hero-section-subtitle wow fadeInUp" data-wow-delay="0.3s">
              Team 19 – UCL Computer Science
              <br/>Hamza Nasir · Karan Chawla · Jamie Weigold
            </p>
            <a
              href="#"
              class="default-outline-btn wow fadeInUp"
              data-scroll-nav="1"
              data-wow-delay="0.5s"
              id="downloadBtn"
            >
              Learn More
              <i class="fa fa-angle-right ml-2"></i>
            </a>
            <a
              href="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
              class="default-video-btn popup-youtube wow fadeInUp"
              data-wow-delay="0.5s"
            >
              <i class="fa fa-play"></i>
            </a>
          </div>
          <!--// .col //-->
          <div class="col-lg-5 hero-image text-right wow fadeInRight">
            <img src="images/home/" class="img-fluid img-jump">
          </div>
          <!--// .col //-->
        </div>
        <!--// .row //-->
      </div>
      <!--// .container //-->
      <a href="#" data-scroll-nav="1" class="down-scroll">
        <i class="fa fa-arrow-down"></i>
      </a>
      <!--// .down-scroll //-->
    </section>
    <!--// Hero Section End  //-->

    <!--//  The problem Section Start //-->
    <section class="services section-padding" data-scroll-index="1" id="services-area">
      <div class="container">
        <div class="row justify-content-center">
          <div class="col-lg-7">
            <div class="section-heading">
              <h2 class="section-title">
                The
                <span>Problem</span>
              </h2>
              <p class="section-sub-title">
                NHS clinicians have no reliable, centralised mechanism to gather Patient Reported Outcome Measures (PROMs) per individual and to understand the factors that help and hinder an individual from adherence to set treatment plans.
                This problem doesn't just exist in the NHS. Reported outcomes and subsequent analysis are a vital feedback mechanism in numerous disciplines, from classrooms to hospital wards.
              </p>
            </div>
          </div>
          <!--// .col //-->
        </div>
        <!--// .row //-->
        <div class="row align-items-center justify-content-center">
          <div
            class="col-lg-4 col-md-6 col-sm-6 services-resp-margin wow fadeInUp"
            data-wow-delay="0.1s"
          >
            <div class="services-item item-shadow">
              <div class="services-icon services-blue-icon">
                <span class="mdi mdi-alert-circle"></span>
              </div>
              <div class="services-body">
                <h5>Slow</h5>
                <p>
                PROMs are typically collected by mailing paper questionnaires to patients. The NHS reports that for a single group of patients, PROMs data can take up to a year to collect.
                </p>
              </div>
            </div>
          </div>
          <!--// .col //-->
          <div
            class="col-lg-4 col-md-6 col-sm-6 services-resp-margin wow fadeInUp"
            data-wow-delay="0.3s"
          >
            <div class="services-item item-shadow">
              <div class="services-icon">
                <span class="mdi mdi-alert-circle"></span>
              </div>
              <div class="services-body">
                <h5>Necessary</h5>
                <p>
                It is becoming increasingly important for doctors to continue monitoring the health of their patients after they've been discharged. Many hospitals are now mandated to do so.
                </p>
              </div>
            </div>
          </div>
          <!--// .col //-->
          <div
            class="col-lg-4 col-md-6 col-sm-6 services-resp-margin wow fadeInUp"
            data-wow-delay="0.3s"
          >
            <div class="services-item item-shadow">
              <div class="services-icon">
                <span class="mdi mdi-alert-circle"></span>
              </div>
              <div class="services-body">
                <h5>Difficult to Analyse</h5>
                <p>
                Collecting responses of physical questionnaires means manually updating records - providing no quick and easy visualisations to assist in analysing the repsonse data.
                </p>
              </div>
            </div>
          </div>
          <!--// .col //-->
        </div>
        <!--// .row //-->
      </div>
      <!--// .container //-->
    </section>
    <!--// The problem Section End //-->

    <!--// Solution Section Start //-->
    <section class="about section-padding" data-scroll-index="2" id="about">
      <div class="container">
        <div class="row align-items-center">
          <div class="col-md-5 col-lg-6 wow fadeInLeft text-left" style="position: relative;">
            <div style="transform: translateX(-100px)">
              <img src="images/home/surveyor_dashboard.png" class="img-fluid img-jump">
            </div>
          </div>
          <!--// .col //-->
          <div class="col-md-7 col-lg-6 wow fadeInUp">
            <div class="about-inner">
              <span class="section-badge">Our Solution</span>
              <h3>Web-based solution to capturing user-reported outcomes</h3>
              <p></p>
            </div>
            <div class="about-list">
              <ul>
                <li>
                  <i class="fa fa-check"></i>
                  Clinicians can assign tasks to groups
                </li>
                <li>
                  <i class="fa fa-check"></i>
                  Patients can report the outcomes of these tasks
                </li>
                <li>
                  <i class="fa fa-check"></i>
                  Progress visualisations provided for both clinicians and patients
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section>
      <div class="container">
        <div class="features-row features-row-mt">
          <div class="row align-items-center justify-content-between">
            <div class="col-md-7 col-lg-6 about-content-wrap wow fadeInLeft">
              <div class="features-inner">
                <span class="section-badge">Key Features</span>
                <h3>Collect & Analyse Results</h3>
                <p>Lorem ipsum</p>
                <ul class="features-list">
                  <li class="d-flex align-items-center">
                    <i class="mdi mdi-file-document"></i>
                    <div class="features-box">
                      <h6>Submit New Tasks</h6>
                      <span>Completely digitize the process of distributing PROMs and collecting their responses.</span>
                    </div>
                  </li>
                  <li class="d-flex align-items-center">
                    <i class="mdi mdi-account-check"></i>
                    <div class="features-box">
                      <h6>Gather Responses</h6>
                      <span>Both quantitative and qualitative responses can be collected for a given task.</span>
                    </div>
                  </li>
                  <li class="d-flex align-items-center">
                    <i class="mdi mdi-chart-arc"></i>
                    <div class="features-box">
                      <h6>Visualise Results</h6>
                      <span>Results are aggregated per group, giving clinicians the ability to analyse progress for both individuals and groups as a whole.</span>
                    </div>
                  </li>
                </ul>
              </div>
            </div>
            <!--// .col //-->
            <div
              class="col-md-5 col-lg-6 text-center features-image-order features-image-resp wow slideInRight"
            >
              <div class="features-circle"></div>
              <div class="feature-image-wrap wow zoomIn" data-wow-delay="0.8s">
                <img src="images/home/task_overview.png" class="img-fluid img-jump">
              </div>
            </div>
            <!--// .col //-->
          </div>
          <!--// .row //-->
        </div>

        <!--        ROW 2-->

        <div class="features-row features-row-mt">
          <div class="row align-items-center justify-content-between">
            <div
              class="col-md-5 col-lg-5 text-center features-image-order features-image-resp wow slideInLeft"
            >
              <div class="features-circle"></div>
              <div class="feature-image-wrap wow zoomIn" data-wow-delay="0.8s">
                <PhoneFrame imgSrc="images/home/response_mobile.png" class="img-fluid img-jump"></PhoneFrame>
              </div>
            </div>
            <!--// .col //-->
            <div class="col-md-7 col-lg-6 about-content-wrap wow fadeInRight">
              <div class="features-inner">
                <span class="section-badge">Key Features</span>
                <h3>Lorem ipsum</h3>
                <p>Lorem ipsum</p>
                <ul class="features-list">
                  <li class="d-flex align-items-center">
                    <i class="mdi mdi-account-lock"></i>
                    <div class="features-box">
                      <h6>Lorem ipsum</h6>
                      <span>Lorem ipsum</span>
                    </div>
                  </li>
                  <li class="d-flex align-items-center">
                    <i class="mdi mdi-qrcode-scan"></i>
                    <div class="features-box">
                      <h6>Lorem ipsum</h6>
                      <span>Lorem ipsum</span>
                    </div>
                  </li>
                  <li class="d-flex align-items-center">
                    <i class="mdi mdi-format-list-bulleted"></i>
                    <div class="features-box">
                      <h6>Lorem ipsum</h6>
                      <span>Lorem ipsum</span>
                    </div>
                  </li>
                </ul>
              </div>
            </div>
            <!--// .col //-->
          </div>
          <!--// .row //-->
        </div>
      </div>
    </section>

    <!--// video Section Start //-->
    <section
      id="how-it-works"
      class="how-it-works-section jarallax bg-gradient-green section-padding"
      data-jarallax
      data-speed="0.3s"
      style="margin-top: 60px;background: #0033CC;"
    >
      <div class="jarallax-img how-it-works-bg"></div>
      <div class="container">
        <!--// .row //-->
        <div class="row justify-content-center align-items-center how-it-work-wrap">
          <div class="col-lg-7 col-md-10 col-sm-12">
            <div class="how-it-works-inner text-center">
              <h3 class="text-white">Video Goes Here?</h3>
              <p>Lorem ipsum</p>
              <div class="how-it-work-video">
                <iframe
                  width="622"
                  height="350"
                  src="https://www.youtube.com/embed/dQw4w9WgXcQ"
                  frameborder="0"
                  allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
                  allowfullscreen
                ></iframe>
              </div>
            </div>
          </div>
        </div>
        <div class="how-it-work-process">
          <div class="row text-center">
            <div class="col-lg-3 col-md-6 col-sm-6 how-it-work-item">
              <div class="how-it-work-number">
                <a>
                  <span>01</span>
                </a>
              </div>
              <h6>Team and Background Introduction</h6>
              <div class="how-it-work-text">
              </div>
            </div>
            <div class="col-lg-3 col-md-6 col-sm-6 how-it-work-item">
              <div class="how-it-work-number">
                <a>
                  <span>02</span>
                </a>
              </div>
              <h6>Technical Overview</h6>
              <div class="how-it-work-text">
              </div>
            </div>
            <div class="col-lg-3 col-md-6 col-sm-6 how-it-work-item">
              <div class="how-it-work-number">
                <a>
                  <span>03</span>
                </a>
              </div>
              <h6>Demonstration and Code Review</h6>
              <div class="how-it-work-text">
              </div>
            </div>
            <div class="col-lg-3 col-md-6 col-sm-6 how-it-work-item">
              <div class="how-it-work-number">
                <a>
                  <span>04</span>
                </a>
              </div>
              <h6>Achievements and Summaries</h6>
              <div class="how-it-work-text">
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="our-team-section section-padding">
      <div class="container">
        <div class="row justify-content-center">
          <div class="col-lg-7">
            <div class="section-heading">
              <h2 class="section-title">
                About the
                <span>Team</span>
              </h2>
              <p class="section-sub-title"></p>
            </div>
          </div>
          <!--// .col //-->
        </div>
        <!--// .row //-->
        <div class="row">
          <div
            class="col-md-4 col-sm-12 text-center team-card-margin wow fadeInLeft"
            data-wow-delay="0.2s"
          >
            <div class="team-card item-shadow">
              <div class="team-img">
                <img src="images/bg/hamza.png" alt="Team image" class="img-fluid" />
                <ul class="team-social">
                  <li>
                    <a href="https://github.com/h-nasir">
                      <i class="fab fa-github"></i>
                    </a>
                  </li>
                </ul>
              </div>
              <div class="team-card-content">
                <h5 class="title">Hamza Nasir</h5>
                <div class="email">
                  <a href="mailto:hamza.nasir.19@ucl.ac.uk">hamza.nasir.19@ucl.ac.uk</a>
                </div>
                <span class="desc">BSc Computer Science Student @ UCL</span>&nbsp;
              </div>
            </div>
          </div>
          <!--// .col //-->
          <div
            class="col-md-4 col-sm-12 text-center team-card-margin wow fadeInUp"
            data-wow-delay="0.4s"
          >
            <div class="team-card item-shadow">
              <div class="team-img">
                <img src="images/bg/karan.jpeg" alt="Team image" class="img-fluid" />
                <ul class="team-social">
                  <li>
                    <a href="https://github.com/1kc2">
                      <i class="fab fa-github"></i>
                    </a>
                  </li>
                </ul>
              </div>
              <div class="team-card-content">
                <h5 class="title">Karan Chawla</h5>
                <div class="email">
                  <a href="mailto:karan.chawla.19@ucl.ac.uk">karan.chawla.19@ucl.ac.uk</a>
                </div>
                <span class="desc">BSc Computer Science Student @ UCL</span>&nbsp;
              </div>
            </div>
          </div>
          <!--// .col //-->
          <div
            class="col-md-4 col-sm-12 text-center team-card-margin wow fadeInDown"
            data-wow-delay="0.6s"
          >
            <div class="team-card item-shadow">
              <div class="team-img">
                <img src="images/bg/jamie.jpeg" alt="Team image" class="img-fluid" />
                <ul class="team-social">
                  <li>
                    <a href="https://github.com/jweig0ld">
                      <i class="fab fa-github"></i>
                    </a>
                  </li>
                </ul>
              </div>
              <div class="team-card-content">
                <h5 class="title">Jamie Weigold</h5>
                <div class="email">
                  <a href="mailto:jamie.weigold.19@ucl.ac.uk">jamie.weigold.19@ucl.ac.uk</a>
                </div>
                <span class="desc">BSc Computer Science Student @ UCL</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
    <!--// Our Team Section End //-->

    <!--// Download Section Start //-->
    <section class="testimonial-section-bg download-wrap section-padding">
      <div class="container">
        <div class="row justify-content-between align-items-center">
          <div class="col-lg-6 download-image wow slideInLeft">
            <img src="images/logo.png" style="max-width: 50%" class="img-fluid" />
          </div>
          <!--// .col //-->
          <div class="col-lg-6 col-md-12 col-sm-11 col-xs-12 wow fadeInUp" data-wow-delay="0.3s">
            <div class="download-section-inner">
              <h2>Lorem ipsum</h2>
              <p>
                Lorem Ipsum is simply dummy text of the printing and typesetting industry.
              </p>

              <div class="download-buttons d-flex justify-content-start">
                <a href="#/guide" class="download-btn">
                  <i class="fa fa-external-link-alt"></i>
                  <span>Launch</span>
                  <span>Activity League</span>
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import PhoneFrame from "../components/PhoneFrame.vue";
export default {
  name: "home",
  components: {
    PhoneFrame
  }
};
</script>

<style scoped>
.email {
  padding-bottom: 20px;
}
</style>