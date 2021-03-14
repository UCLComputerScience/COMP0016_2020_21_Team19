<template>
    <div>
    <PageTitle title="Human Computer Interaction"></PageTitle>


    <!-- hand drawn sketches-->
    <section class="section">
        <div class="container">
            <div class="row">
                <div class="col-lg-10 mx-auto text-center">
                    <h3 class="section-title"><span>Sketches</span></h3>
                    <img src="images/" class="img-responsive" style= "width: 90%;">
                    <img src="images/" class="img-responsive" style= "width: 90%;">
                    <img src="images/" class="img-responsive" style= "width: 50%;">
                    <img src="images/" class="img-responsive" style= "width: 50%;">
                    <img src="images/" class="img-responsive" style= "width: 90%;">
                    <img src="images/" class="img-responsive" style= "width: 90%;">
                    <img src="images/" class="img-responsive" style= "width: 90%;">
                </div>
            </div>
        </div>
    </section>
    <!-- /head drawn sketch -->

        <!-- design principle-->
        <section class="section">
            <div class="container">
                <div class="row">
                    <div class="col-lg-10 mx-auto text-center">
                        <h3 class="section-title">Lorem ipsum</h3>
                    </div>
                    <div class="col-md-4">
                        <img
                                src="images/"
                                class="img-responsive alignright"
                                style="width: 100%;"
                        />
                    </div>

                    <div class="col-md-8">
                        <div class="bg-gray p-5 mb-4">
                            <div class="media border-bottom py-4">
                                <div class="media-body">
                                    <h4 class="mt-0">Lorem ipsum</h4>
                                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc porttitor tempus vehicula.
                                </p>
                                </div>
                            </div>
                        </div>
                        <div class="bg-white p-5 mb-4">
                            <div class="media-body">
                                <h4 class="mt-0">Lorem</h4>
                                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc porttitor tempus vehicula.</p>
                            </div>
                        </div>
                    </div>
                </div>


                <div class="bg-gray p-5 mb-4">
                    <div class="media-body">
                        <h4 class="mt-0">Lorem</h4>
                        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc porttitor tempus vehicula.</p>
                    </div>
                </div>


                <div class="bg-white p-5 mb-4">
                    <div class="media py-4">
                        <div class="media-body">
                            <h4 class="mt-0">Lorem</h4>
                            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc porttitor tempus vehicula.</p>
                        </div>
                    </div>
                </div>
                <div class="bg-gray p-5 mb-4">
                    <div class="media py-4">
                        <div class="media-body">
                            <h4 class="mt-0">Lorem</h4>
                            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc porttitor tempus vehicula.</p>
                        </div>
                    </div>
                </div>

            </div>
        </section>
        <!--/ Design principles-->


    <!-- prototype-->
        <section class="section">
            <div class="container">
                <div class="row">
                    <div class="col-lg-10 mx-auto text-center">
                        <h3 class="section-title"><span>Prototypes</span></h3>

                        <carousel :perPage="1" :navigationEnabled="true">
                            <slide v-for="n in 6" v-bind:key="n">
                                <!-- <img :src="'images/xd/web'+n+'.png'" class="img-responsive slideImg item-shadow"> -->
                            </slide>
                        </carousel>
                        <!--// .screenshots-slider-wrap //-->
                    </div>
                </div>
            </div>
        </section>


        <section class="section">
            <div class="container">
                <div class="row">
                    <div class="col-lg-10 mx-auto text-center">
                        <h3 class="section-title">HCI<span>Slides</span></h3>

                        <iframe src="https://docs.google.com/presentation/d/e/2kjhnkjhhc/embed?start=false&loop=true&delayms=60000" frameborder="0" width="100%" height="547" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>

                    </div>
                </div>
            </div>
        </section>

    <!-- /prototype -->
        </div>
</template>

<script>
    import PageTitle from '../components/PageTitle.vue'
    import { Carousel, Slide } from 'vue-carousel';
    export default {
        name: "hci",
        components: {
            PageTitle,
            Carousel,
            Slide
        }
    }
</script>

<style scoped>
    .slideImg{
        max-height: 500px;
    }
</style>