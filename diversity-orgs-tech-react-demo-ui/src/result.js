import React from "react";
import PropTypes from "prop-types";

function Result(
    props,
    ...rest) {
    const hasLink = <a 
    href={props?.result?.url?.raw}
    onClick={props.onClickLink}
    >
          {props?.result?.name?.raw}
        </a>

    const noLink = props?.result?.name?.raw

    function parentOrg () { 
        if (props?.result?.parent_organization?.snippet) {
            return <small className="parentOrg mx-2"><a href={props.result?.global_org_url_from_parent_organization?.raw}>{props.result.parent_organization.raw}</a></small>
        }

        return ''
    }

    function smallDivs (field) {
        return field ? <small className="mx-2">{field}</small> : ''
    }

    function linkOption () {
        const links = [];
        const name = props?.result?.name?.raw;

        if (props?.result?.donate?.raw) {
            const donate = props?.result?.donate?.raw;
            const donateAlt = "donate" + name;
            links.push(<a href={donate}>
                   <img
                    className="mx-4 w-6 font-green-200 stroke-current rounded shadow"
                    src="/heroicons/optimized/outline/currency-dollar.svg"
 alt={donateAlt}/> 
                </a>)

        }

        if (props?.result?.links?.raw){

            for (let link of props?.result?.links?.raw) {
                
                if (link.includes('twitter.com')) {
                    const twAlt = "twitter " + name;
                   links.push(<a href={link}><img alt={twAlt} src="https://ik.imagekit.io/cxazzw3yew/Twitter_icon_square_logo.jpg" className="mx-4 w-6 rounded shadow" /></a>)
                    }

                if (link.includes('meetup.com')) {
                    links.push(<a href={link}><img alt="meetup + {props.result.name.raw}" className="mx-4" src="https://ik.imagekit.io/cxazzw3yew/meetup-logo-m-swarm-thumb.jpg" className="mx-4 w-6 rounded shadow" /></a>)
                }

                if (link.includes('facebook.com')) {
                    links.push(<a href={link}><img alt="facebook {props.result.name.raw}" className="mx-4" src="https://ik.imagekit.io/cxazzw3yew/1-facebook-colored-svg-copy-256.png" className="mx-4 w-6 rounded shadow" /></a>)
                }

                if (link.includes('linkedin.com')) {
                    links.push(<a href={link}><img alt="linkedin {props.result.name.raw}" className="mx-4" src="https://ik.imagekit.io/cxazzw3yew/LinkedIn_icon_square_logo.jpg" className="mx-4 w-6 rounded shadow" /></a>)
                }


                if (link.includes('slack')) {
                    links.push(<a href={link}><img alt="slack {props.result.name.raw}" className="mx-4" src="https://ik.imagekit.io/cxazzw3yew/slack.png" className="mx-4 w-6 rounded shadow" /></a>)
                }
            }

        return links
        }
    }


    return <div className="my-4 lg:flex lg:jusitify-between items-center rounded-lg shadow p-6">
            <div className="lg:w-1/4 w-1/4 lg:p-8">
                <img 
                    src={props?.result?.organization_logo?.raw}
                    alt={props?.result?.name?.raw} Logo
                />
            </div>
            <div> 
                {props?.result?.diversity_focus?.raw?.map((o) => smallDivs(o))}
                {parentOrg()}
                <h1 className="text-3xl my-3">{props?.result?.url?.raw ? hasLink : noLink}</h1>
            <div className="flex items-center">
                {smallDivs(props?.result?.city?.raw)}
                {linkOption()}
            </div>
            </div>
        </div>
    } 

Result.propTypes = {
  result: PropTypes.object.isRequired,
  className: PropTypes.string,
  titleField: PropTypes.string,
  urlField: PropTypes.string
};

export default Result;
